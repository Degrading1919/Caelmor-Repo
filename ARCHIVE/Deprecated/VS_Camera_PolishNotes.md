# VS Camera Polish Notes
Caelmor Vertical Slice — UX / UI & NPE Designer  
Focus: smoothing, follow feel, collision behavior, readability for top-down/OTS hybrid

---

# 1. Core Goals for Camera Polish
The VS camera must:
- Maintain **total spatial readability** in a top-down hybrid view.
- Avoid jitter, overshoot, or drifting.
- Always keep the **player silhouette as the visual anchor**.
- Handle collision without sudden “jumps” or disorienting zoom effects.
- Preserve the grounded feel described in the movement spec.

These polish notes adjust smoothing curves, follow behavior, camera anchoring, and collision correction.

---

# 2. Follow Smoothing — Revised Model

## 2.1 Position Smoothing Target Behavior
Current implementation uses:
```csharp
Vector3.Lerp(transform.position, desiredPos, 1f - Mathf.Exp(-Time.deltaTime / positionLag));
This is good, but polish requires:

Improvements
Velocity-based smoothing instead of pure positional springing:

Player movement in Caelmor is intentionally smooth (0.18–0.28s accelerations).

Camera smoothing should mirror this curve without feeling “floaty.”

Micro-lag reduction on direction reversals:

When the player sharply changes direction (common in top-down), the camera should tighten the offset curve by ~10–15%.

Recommendation
Add a dynamic smoothing weight:

If player velocity magnitude changes > 35% within 0.1s, temporarily reduce positionLag by 20%.

Prevents the “rubberband” effect when repositioning.

3. Rotational Readability & Comfort
3.1 Fixed Pitch & Yaw Validation
Current rotation uses a fixed pitch (52°) and no yaw, which is correct for VS readability.
CameraController

Minor Polish
Increase rotationLag from 0.06 → 0.08 for slightly more natural stability.

Because yaw is fixed, smoothing is mostly aesthetic—but too low causes micro-jitter during collision adjustments.

3.2 Subtle Counter-Swing (Optional Future)
Not for VS, but recommended for v1:

A 1–2° counter-swing during sprinting improves motion readability without harming clarity.

4. Collision Handling — Smoother Corrections
Current method:

SphereCast from target to camera.

If blocked, clamp distance and move camera inward.
CameraController

Polish Needed
Hard pops occur if the corrected position is drastically different.

Collision resolution should use interpolation rather than immediate repositioning.

Recommended Approach
Cache the previous uncorrected camera target position.

When a collision occurs:

Lerp from previous position to corrected position using a short easing window (0.06–0.1s).

Prevents sudden zoom-in jolts.

Additional Guidance
Add a "sliding collision" behavior:

When the camera collides horizontally (rare with top-down pitch), let it slide along geometry rather than snapping.

5. Camera Distance Behavior — Refinement of Readability Envelope
VS design mandates:

Default height: 9.5m

Min/max: 8.0–12.5m
VS_MovementAndCamera_Design_v1

Polish Notes
Distance Shift Tolerance

When the player enters cluttered scenery (e.g., farmstead), allow a small auto-raise (≈ +0.3m).

Produces better silhouette visibility.

Tolerance Dampening

Prevent oscillation by enforcing a cooldown (0.5s) before auto-raise re-evaluates.

No Auto-Zoom

Reinforce VS rule: player-controlled zoom only—no dynamic zooming except collision safety adjustments.

6. Player Silhouette Priority
Improve Frame Clarity
When the player is near tall objects, subtly shift camera offset sideways (0.3–0.6m) to expose the silhouette.

Must be subtle to avoid OTS drift.

Trigger only when:

Obstructing mesh is tagged “LargeProp” or “Structure”

Height > camera height - 1.5m

This avoids situations where the player passes closely to barn walls or boundary stones and temporarily becomes visually merged.

7. Readability in Combat Pockets
Top-down readability is essential for VS combat (2–3s windups).
VS_MovementAndCamera_Design_v1

Camera Adjustments for Combat:
Short soft-raise (0.2–0.3m) when 2+ hostiles enter player’s near radius.

No rotation or framing changes—just distance for spatial clarity.

Fade priority props (future polish):

If tall prop obstructs player or enemy silhouettes, fade opacity to 40–60%.

8. Input Responsiveness & NPE Comfort
New players often struggle with:

Overshoot during follow lag

“Swimming” feel when the camera is slow

Sudden pushes inward from collision

Final Recommended Polishing Targets
Position Lag: 0.12 (idle), 0.10 (moving), 0.085 (reversing)

Rotation Lag: 0.08

Collision Correction: 0.06–0.1 Lerp window

Optional offset bias when close to vertical structures: 0.3–0.6m

These values preserve the grounded pace while making the camera feel responsive and trustworthy.

9. Summary of Required Adjustments
Area	Recommended Change
Follow smoothing	Add dynamic weight tied to velocity change
Rotation smoothing	Increase rotationLag slightly to reduce jitter
Collision	Interpolate corrections; avoid pop-in
Distance	Add subtle auto-raise in dense geometry
Silhouette clarity	Offset shift when near tall structures
Combat visibility	Soft-raise when ≥2 enemies near player
Readability	Ensure consistent framing under all movement states

10. Implementation Notes for Coding Assistant
Provide hooks for dynamic smoothing weights.

Add interpolation wrapper for collision-adjusted positions.

Add optional offset-shift module with height threshold.

Ensure the system remains entirely client-side (per VS Tech Spec).

Maintain all pitch/zoom rules from design doc.