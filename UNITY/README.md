# Caelmor playable foundation

Unity **6000.5.5f1**, Windows x64, built-in render pipeline. No external art or paid packages. This is a technical greybox fixture, not the authored Lowmark world or a narrative slice.

## Build and run

Activate Unity Personal in Unity Hub first. From the repository root:

```powershell
./UNITY/Build.ps1
& 'C:/Users/CK/Documents/Caelmor-Build/Caelmor.exe'
```

The script builds the canonical `CODE/Caelmor.Runtime.csproj` in Release, stages its DLL into the ignored Unity plugin directory, creates the scene, runs scene gameplay checks, builds the Windows player, and runs its headless smoke scenario. The executable and both logs are outside the repository in `C:/Users/CK/Documents/Caelmor-Build`. Override with `-OutputDirectory` or `-UnityEditor` as needed. Exit codes and missing smoke success markers fail the script.

For editor play:

```powershell
./UNITY/Build.ps1 -StageOnly
```

Open `UNITY/` in Unity Hub and open `Assets/_Project/World/PlayableFoundation.unity`. The scene and materials were generated and saved by Unity. If the scene is missing, the editor creates it on its first successful import. The **Caelmor** menu can recreate or validate the fixture. Press Play. Stage the DLL again after changing canonical runtime source. Generated DLLs are deliberately ignored; there is one authored runtime source.

## Controls and observable behavior

- **Left click navigable terrain:** set a movement destination. The host computes a complete route around obstacles and follows it until arrival. Click elsewhere to replace the route without an idle interruption. A small ground marker shows the committed destination. **Hold Shift:** sprint along the route, without stamina. No jump input.
- **F3:** toggle optional camera-relative WASD debugging (off at startup). A nonzero WASD command cancels the route; ordinary play uses terrain clicks. Invalid or unreachable replacement clicks preserve an existing valid route.
- **Right mouse + movement:** camera orbit. **Mouse wheel:** player-controlled zoom. Scene collision corrects camera clipping.
- **E:** request interaction with the amber marker. Walk closer until the prompt becomes available. A legal host interaction switches the marker between amber and green, increments the committed count, and shows its authoritative tick. Trying from too far away shows a rejection.
- **Escape:** stop the route and open/close help. The help panel has a Quit button. Help, focus changes and OS pause cancel queued input and the active route. UI panels, obstacle faces, obstacle tops, and non-terrain objects never become click destinations.

Boundary walls and two internal obstacles exercise swept host collision and native NavMesh pathfinding. If geometry changes after the mesh was baked and blocks a route, the host stops safely and asks for a new destination; automatic dynamic mesh rebuilding is outside this fixture. The static ground is flat; multi-level traversal and off-mesh links are not implemented. The avatar is a presentation capsule; it has no authoritative collider or movement scripts. The HUD shows host tick, committed position and interaction state. Presentation interpolates committed snapshots; there is no prediction. Fresh sessions reset on exit; persistence to disk is not implemented by this fixture.

## Runtime ownership

`PlayableHost` composes the existing `WorldSimulationCore`, `AuthoritativeCommandIngestor`, command freeze/consume hooks, `PlayerSaveBindingSystem`, `PlayerSaveRestoreSystem`, `PlayerSessionSystem`, `PlayerRuntimeInstanceManager`, `PlayerZoneResidencySystem` and `PlayerLifecycleSystem`.

The Unity main thread owns the host and physics. A scheduler invokes `WorldSimulationCore.ExecuteSingleTick()` every 100 ms; the core owns authoritative tick indices and fixed deltas. The dedicated background driver is intentionally not started alongside it. A frame may execute at most three catch-up ticks, then discards excess wall time. Each input batch contains quantized destination X/Z, optional debug direction, sprint intent or interaction target ID only. A destination never supplies client position or a client-computed path. `TerrainNavigation` validates designated ground, small mesh projection tolerance, and `PathComplete` on the host; it never uses a `NavMeshAgent` to move actors. The scene-baked `PlayableNavigation.asset` uses radius clearance greater than the physical capsule plus its collision skin. Persistent waypoints are advanced only by authoritative ticks, with exact speed budgets across corners and no overshoot at arrival. The host stamps tick and sequence, validates real session/restore/lifecycle/residency gates, normalizes movement, sweeps collision, and checks target availability, zone, distance and line of sight. Working state commits in `OnPostTick`, before snapshot publication and interaction events. Inactive or nonresident sessions receive neither client snapshots nor interaction events. Client presentation never changes authoritative position or marker state.

The fixture's server initializes a fresh in-memory save through the real restore state machine; an unknown save cannot complete restore. Scene-authored spawn, zone 1, marker 9001, geometry, movement speeds and reach are explicitly technical test values. They are not production placements, canonical tuning, NPC definitions, economy rules or quest data. No content definitions are generated by gameplay code.

## Narrative entry

The scene reserves **Narrative entry / reserved for approved Lowmark content**. A later approved narrative adapter can subscribe to `PlayableBootstrap.HostInitialized`, then `PlayableHost.InteractionCommitted(session, targetId, tick)` and `SnapshotCommitted`. Interaction acknowledgment is emitted only after a legal committed state change. These are integration hooks, not quest acceptance, dialogue, rewards or objective progression. Bind authored content IDs, NPC residency and the existing quest/onboarding runtime through their approved contracts when implementing the first narrative; the marker must remain a fixture until then.

## Validation

The build executes `PlayableValidation` against real Unity colliders and host commands. It checks deferred mutation, 100 ms movement, normalized debug diagonals, sprint, missing-debug-input stop, non-finite rejection, lifecycle suspension, residency loss, unknown and cross-zone interaction targets, reach, line of sight, bounds, input cancellation, and exactly-once events after snapshot commit. Navigation assertions use the real wall and native mesh: route around the obstacle to the requested endpoint, keep following without held input, replace a destination while moving, reject blocked/off-terrain/elevated/non-finite destinations, reject a physically navigable but disconnected mesh island, stop at newly introduced collision, cancel routes across focus/lifecycle boundaries, and interact successfully after arrival. The scene is reopened before validation and the standalone repeats these checks, proving the serialized mesh/ground markers load correctly. The standalone `--caelmor-smoke` mode repeats these checks and verifies the real-time scheduler advances 10–13 ticks in 1.15 seconds, then returns exit code 0 and `CAELMOR_SMOKE_PASSED`.

An SDK source check can be run independently after staging/building the runtime:

```powershell
./UNITY/Tools/Compile-Source.ps1
```

This checks runtime and editor adapter C# against the installed Unity assemblies. It cannot verify engine import, scene rendering, physics execution or a player build. Those require a licensed Unity Editor.

Verified on 2026-11-01 with Unity 6000.5.5f1: source check passed with zero warnings/errors; licensed editor import, scene gameplay checks and Windows x64 build succeeded. The initial WASD executable was manually playtested by the Creative Director: collision, camera and interactions worked.

The click-to-move build was regenerated and verified in the licensed editor and actual Windows player: baked NavMesh/ground markers survived scene reopen, all navigation/gameplay assertions passed, and the standalone scheduler advanced 12 ticks in 1.15 seconds with exit code 0. Evidence is in `unity-build.log` and `standalone-smoke.log` beside the executable.

Standalone pointer and visual verification also passed: left-click terrain navigation and arrival stopping, a destination beyond the large obstacle, E interaction after arrival, and a click on the host-status HUD that left the position and route unchanged. These checks supplement the engine tests; they are not a full usability or long-session playtest.
