# Stage 10.4 — Combat Authority and Networking Contract
**Scope:** Authority boundaries + networking implications only  
**Combat:** Server-authoritative, deterministic, tick-aligned (10 Hz), schema-first  
**Dependencies:** Stage 10.1 (Intents), Stage 10.2 (State Model), Stage 10.3 (Resolution + Contracts), Phase1_4 Technical Foundation

This document defines **who owns the truth** in combat.
It locks what the client may submit, what the server alone resolves, what is observable vs authoritative, and what must never be predicted or replayed.

This document does NOT define:
- Networking implementation details (protocols, transport, RPC layouts)
- Rollback, reconciliation, or prediction algorithms
- Animation, UI, physics, or client presentation rules
- Persistence schema changes

---

## 1) Authority Ownership Matrix

The following matrix defines authority for combat categories.

### Legend
- **Client-authoritative:** Client may determine truth for this category
- **Server-authoritative:** Server is sole source of truth
- **Client-observable only:** Client may receive and display, but never author
- **Never exposed:** Not sent to clients as authoritative data (may exist server-side only)

---

### 1.1 Combat Intents
- **Authority:** **Client-submittable / Server-authoritative acceptance**
- **Client-authoritative:** None (client may request; cannot declare accepted truth)
- **Server-authoritative:** Acceptance/rejection, queue inclusion, ordering, legality gate outcome
- **Client-observable only:** Receipt acknowledgement and final disposition (accepted/rejected/nullified/canceled) as reported by server
- **Never exposed:** Server-side validation reasoning beyond minimal reason codes (implementation-defined; not a tuning surface)

**Meaning:** Clients can **submit** intents. Only the server can declare whether an intent is real (accepted/queued) and how it is processed.

---

### 1.2 Combat State
- **Authority:** **Server-authoritative**
- **Client-authoritative:** None
- **Server-authoritative:** Entire combat state model and state transitions
- **Client-observable only:** State snapshots and transition notifications as replicated by server
- **Never exposed:** Internal intermediate evaluation artifacts used during resolution phases

**Meaning:** Combat state is never computed on the client. The client only observes server-published state.

---

### 1.3 Damage Outcomes
- **Authority:** **Server-authoritative**
- **Client-authoritative:** None
- **Server-authoritative:** All damage records (creation, ordering, disposition, application)
- **Client-observable only:** Damage outcomes as reported by server (including applied/not-applied disposition and reason codes)
- **Never exposed:** Raw calculation internals or any formula inputs not explicitly included in the published outcome contract

**Meaning:** The client never predicts damage and never claims damage happened. Only server outcomes are truth.

---

### 1.4 Mitigation Results
- **Authority:** **Server-authoritative**
- **Client-authoritative:** None
- **Server-authoritative:** Mitigation results per damage instance (modified/unchanged/nullified, with reason code)
- **Client-observable only:** Mitigation results as reported by server
- **Never exposed:** Internal mitigation evaluation steps or hidden state used to compute mitigation

**Meaning:** Mitigation is a resolution product, not a client capability.

---

### 1.5 Cancellation Results
- **Authority:** **Server-authoritative**
- **Client-authoritative:** None
- **Server-authoritative:** Whether cancellation is accepted, whether referenced action is cancelable, and final cancel disposition
- **Client-observable only:** Cancellation disposition and reason code as reported by server
- **Never exposed:** Any rule evaluation beyond minimal reason codes

**Meaning:** Cancellation is only a request from the client; success is declared later by the server.

---

### 1.6 Restore State
- **Authority:** **Server-authoritative**
- **Client-authoritative:** None
- **Server-authoritative:** Hydration of combat-relevant state after reconnect/restore, and publication of the current authoritative snapshot
- **Client-observable only:** The post-restore snapshot provided by server
- **Never exposed:** Any replay trace, event journal, or partial tick state (must not exist as a dependency)

**Meaning:** Restore is hydration only. No combat logic is replayed on either side.

---

## 2) Client Responsibilities

### 2.1 What the Client May Submit
The client may submit only **combat action intents** defined in Stage 10.1, containing only fields permitted by that intent contract.

Client submissions are:
- Requests to act
- Not claims of success
- Not authoritative ordering

---

### 2.2 What the Client May Cache
The client may cache:
- The most recent authoritative combat state snapshot received from the server
- Server acknowledgements and disposition results for previously submitted intents
- Server-published damage and mitigation outcome records

Client caches are:
- Non-authoritative
- Replaceable by newer server snapshots at any time
- Not valid inputs to local combat resolution

---

### 2.3 What the Client May Display Optimistically
Policy-level rule:
- The client may display **only local intent submission status** (e.g., “submitted / awaiting server”) as a UI concern.
- The client must not display any *outcome* optimistically (no predicted damage, mitigation, state transitions, or cancel success).

This stage does not define UI behavior; it defines that **outcome optimism is not permitted**.

---

### 2.4 What the Client Must Never Resolve or Predict
The client must never:
- Resolve combat outcomes
- Predict damage
- Predict mitigation
- Predict cancel success
- Advance combat state
- Apply health/condition changes based on local inference
- Re-run combat resolution after reconnect or restore

The client is an input device and an observer, not a simulator.

---

## 3) Server Responsibilities

### 3.1 What the Server Alone Validates
The server alone validates:
- Intent structure completeness
- Submitting entity authority
- Referential validity (targets/keys exist)
- Tick-acceptance window (no mid-tick acceptance)
- Any legality gates against authoritative combat state

Invalid submissions are rejected before queuing.

---

### 3.2 What the Server Alone Orders
The server alone determines deterministic ordering:
- Per tick ordering of intents
- Conflict selection boundaries
- Cancellation evaluation ordering (as a request stream, not a guarantee)

Client arrival order is not authoritative.

---

### 3.3 What the Server Alone Resolves
The server alone resolves:
- Combat resolution phases per tick (as defined in Stage 10.3)
- State transitions
- Damage outcomes
- Mitigation results
- Final disposition of intents, including cancellation success/failure

---

### 3.4 What the Server Persists
This stage does not change persistence.
However, the server remains the sole owner of:
- Any persisted combat-relevant state that exists in the locked combat state model and technical foundation
- Checkpoint-boundary commit discipline
- No mid-tick persistence commits

If combat state is persisted, it is persisted only at valid checkpoint boundaries, and restored via hydration only.

---

### 3.5 What the Server Restores
On reconnect/restore, the server:
- Hydrates authoritative state (no replay)
- Publishes a current authoritative snapshot to the client
- Does not attempt to “catch up” by replaying combat logic
- Does not accept client-provided history as truth

---

## 4) Networking Guarantees & Non-Guarantees

### 4.1 Guarantees
- **Single authority:** The server is the only combat truth source.
- **Tick spine:** Combat resolution occurs on the authoritative 10 Hz server tick.
- **Deterministic ordering:** The server provides deterministic ordering independent of client arrival time.
- **No replay on restore:** Restore is hydration only; no combat events are replayed.
- **No mid-tick mutation:** State changes occur only through server tick resolution phases.

---

### 4.2 Non-Guarantees (Intentional)
- No guarantee of low latency
- No guarantee of in-order arrival from clients
- No guarantee that an accepted intent will succeed
- No guarantee that cancellation will succeed
- No guarantee that clients will observe intermediate resolution steps
- No guarantee of identical “moment-to-moment feel” across clients (presentation is out of scope)

---

### 4.3 Preserving Determinism Across Reconnects and Restores
Determinism is preserved by:
- Server-owned tick advancement
- Deterministic ordering rules
- Hydration-only restore (no replay)
- Explicit, server-published authoritative snapshots after reconnect
- No dependence on client history, timestamps, or wall-clock time for resolution

Clients may reconnect at any time and re-enter combat observation via the latest server snapshot.

---

## 5) Explicit Prohibitions (Forbidden Behaviors)

The following behaviors are explicitly forbidden by contract:

### 5.1 Client-Side Resolution and Prediction
- Client-side combat resolution of any kind
- Client-side damage prediction
- Client-side mitigation prediction
- Client-side cancel success prediction
- Client-side authoritative state transitions

### 5.2 Mid-Tick Mutation
- Any combat state mutation outside the authoritative server tick phases
- Any acceptance or resolution of intents mid-tick
- Any persistence commit mid-tick

### 5.3 Replay on Restore
- Replaying combat logic on restore (server or client)
- Re-applying damage outcomes from a journal
- Re-simulating missed ticks from client-provided inputs

### 5.4 Auto-Correction
- Auto-retargeting invalid intents
- Auto-converting one intent into another
- Auto-retrying intents
- Inferring outcomes from partial data

Failures must remain explicit, deterministic, and server-declared.

---

## Explicit Non-Goals (Reaffirmed)
This stage does NOT define:
- Transport protocols, message formats, or RPC endpoints
- Prediction, rollback, or reconciliation approaches
- UI or animation behavior
- Persistence changes or save formats

---

## Exit Condition
Stage 10.4 is complete when:
- Authority ownership is unambiguous for every combat category
- Client responsibilities are constrained to submission + observation
- Server responsibilities are constrained to validation + ordering + resolution + snapshot publication
- Networking guarantees and non-guarantees preserve determinism under latency, reconnects, and restore
- Prohibited behaviors are explicitly stated
