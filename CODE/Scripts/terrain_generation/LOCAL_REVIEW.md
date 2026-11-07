# Lowmark local geography review

**Review baseline:** verified `main` / `origin/main` at `3ec4003`. The new local-refinement mission preserves the approved regional composition. This review does not move anchors, rewrite quests, approve building sites or explain anomalous water. Numerical observations below come from the committed 8 m arrays and controls; subsequent 2 m results must be reported separately.

The current dossier and POI package were also retrieved from GitHub `main` through the connected integration. Their returned blob identities were `f2fc6f932e6a0280130bf3cff474a17355615b96` and `a26c3a9f593ff98a9a3fc676f3877023e7c0448f`. Canonical UTF-8/LF fingerprints for the eight consulted repository texts are recorded in `local_controls.json`.

## Crestbridge: what the sources actually require

| Authority / source | Required relationship |
|---|---|
| Regional dossier IV.4, lines 168–176; V.2, 222–234 | A reinforced central river crossing; Crest Hall watches the bridge/roads; town clusters around the crossing. These statements do not impose a numeric Hall distance. |
| Narrative Production Bible P02/P07, lines 129–134; MQ2, 236; D-11, 101 | Bridge, tolls, granaries and Hall form one reused civic POI; the Depot is in the hill behind the granaries. New narrative details remain proposals until reviewed. |
| POI requirements P02/P07, lines 83–93 and 143–153 | Waiting wall faces granary yard and south toll; granary undercroft connects to the hill passage; Depot chute reaches a slack river backwater below the toll. Hall's water-gate opens to the river above the Cut mouth. |
| POI requirements §6.1, lines 438–457 | Near means a short walk with view/earshot. Granaries have Depot behind them, Hall beside them and an undercroft connection; bridge north stair emerges near Hall's water-gate wall. |
| Main Act I A5.1–A5.2, lines 129–153; S07/S08, 228–239 | Cart-rutted passage runs from granary undercroft into the depot; chute gallery has a river ledge/return shortcut. The player returns to the yard for the next draw. |
| Main Act III §10.3, lines 134–147 | Hall stands on the riverbank; barges unload directly beneath it. The low Granary Passage links Corvin's undercroft; water-gate basin and 14 × 8 m landing are local parts of the Hall complex. |
| Night Bridge NB.2, lines 352–364 | Traversal follows the bridge underside to a north stair close to the Hall water-gate wall. Main Act III line 248 additionally wants a short towpath walk from Hall's bank to the Cut mouth. |

The detailed quest/POI statements are authored requirements, including explicit map-verification flags. They must not silently override the newer approved map placement; conversely, passing a road-grade check does not prove those requirements work.

### Measured conflict

| Pair / location | Baseline observation |
|---|---:|
| Town anchor → Hall | 652.28 m straight; retained candidate road 652.62 m |
| Town anchor → Depot | 779.42 m straight |
| Hall → Depot | 403.70 m straight; candidate access 407.31 m |
| Regional `crest` river node → Hall | 679.49 m |
| Hall → nearest retained natural river | 640.31 m |
| Depot → nearest retained natural river | 836.62 m |
| Hall / Depot ground at nearest 8 m sample | 70.02 / 67.24 m |
| Regional crossing water stage / bed | 63.10 / 61.90 m |

The earlier approximate Hall figure was 648 m; recalculation from the saved normalized coordinates gives 652.28 m. It is the same mapped relationship, not a new relocation. At the fixture's provisional 3 m/s walk, 652 m is 3.62 minutes before detours; those speeds are sensitivity inputs, not approved movement balance.

A distant fortress could still watch a crossing, so distance alone does not contradict the dossier. The hard functional problem is the Hall's roughly 640 m separation from the river: a road cannot make its undercroft directly river-accessible or put the bridge's exit stair beside that water-gate. Likewise, the Depot's symbol is an area reference, not an approved gallery/chute footprint; the existing arrays do not establish the required bank exit. Long subterranean routes are conceivable, but neither their geometry, scale, access nor solo-dev content cost has been approved.

**Depot head/length diagnostic.** Act I A5.2 K–L (lines 150–151) specifies an underground gallery, a stone chute dropping through the hillside, a timber pulley gantry and a high ledge above slack backwater, followed by a short bank/hill-road return. From the fixed Depot symbol's nearest 8 m ground sample (67.2357 m) to the closest retained natural water (the `crest` node, stage 63.1 m), the gross vertical difference is only **4.1357 m over 836.6161 m**, a straight mean fall of **0.4943%**. That closest point is at the toll line, not a verified below-toll backwater. The next defined downstream node, `mill_intake`, is 920.1313 m away at stage 62.9 m: gross head 4.3357 m, mean fall 0.4712%.

These are ground-to-water diagnostics, not chute gradients. Neither gallery intake elevation nor chute/mooring XY is approved; an underground intake could have less head, and an actual route may be longer. The source's pulley supports controlled lowering at a genuine bank exit, not an assumption that grain will gravity-slide nearly a kilometre. No friction, grain-flow, hoist or geotechnical model is claimed, and the figures do not prove all underground arrangements impossible. They demonstrate that the present regional marker does not establish the compact chute/short-exit relationship. No new chute geometry has been added.

**No approved granary XY exists in these sources.** The neutral box near the technical crossing is explicitly a *conceptual yard-location example*, excluded from capacity and grading. It demonstrates an unresolved relationship, not an authored new granary. The Hall box is only a size marker; the small Depot box marks an area/entrance, not a surface warehouse. No fictional waterfront annex, canal or water-gate is added to make the view appear resolved.

### Inspection crossing correction

The regional `crest` hydrology node is not surveyed bridge geometry. The retained `landing_to_crestbridge` route intersects `fen_to_crestbridge` at **[2581.210228, 1556.418001] m**, about 60.31 m from that node, which remains unchanged. The road crosses the local river tangent at about 57.15°. A neutral 72 × 8 m deck proxy follows the retained road and uses a technical 66.115 m deck top above the interpolated 63.115 m stage. These are scale/clearance placeholders, not structural or flood certification.

The eye-level inspection camera sits on the same road 140 m before the intersection, at **[2483.714354, 1455.946341] m**, with its eye 1.75 m above sampled solid terrain. Its baseline open-terrain ground is about 67.30 m. Cameras use true elevation without vertical exaggeration. A separate Mill-access crossing near the regional node remains an unbuilt works gap; one proxy does not certify both crossings.

### Conservative decision options

1. **Keep every regional anchor for this milestone; leave the civic adjacency unresolved.** Refine bounded local roads/banks and show the failed links honestly. Before production layout, the Director decides the Hall/granary/river arrangement. This is the implemented review stance.
2. **Approve a compact civic/waterfront arrangement explicitly.** A Director-approved local map revision could bring the Hall's functional footprint, granaries, north stair and depot bank exit into a coherent crossing compound. Any actual anchor adjustment or reinterpretation of a symbol as a district label must be approved and recorded first; no replacement coordinates are silently proposed as canon here.
3. **Keep fixed remote buildings and revise the authored connection requirements.** Longer storage passages and detached waterfront functions would require explicit quest/location changes and new scope. A new 640 m canal or invented annex is not a routine terrain fix and is not recommended merely to conceal the conflict.

## Five hydrological concerns

| Concern | What currently works / fails | Practical next resolution and authority boundary |
|---|---|---|
| Western Whisperflow arm | Current interpretation is a 1,436.68 m side backwater connected at the weir-downstream node, with standing stage 60.1 m and a small bed fall. The illustration's western termination/return is ambiguous. | Keep it explicitly unresolved during local work. Director confirms terminal backwater versus continuous meander/distributary. A confirmed return requires a real junction and descending profile, followed by full drainage verification; do not invent one to make the graph pass. |
| Fen outlet versus closure | Regional natural outlet toward Crestbridge remains open. Zone line 32 conflicts with Act III 239–247 saying Cut/culvert closure leaves the whole fen without an outlet. | Least geographical disruption is to clarify whether the quest concerns isolated deep storage/Braid pockets rather than all river discharge. That is a Director-reviewed narrative/state interpretation, not an implemented rewrite. Alternatively, approved existing sill/gate controls must be identified and modelled. Do not silently dam the main river or delete its outlet. |
| Mill race and lower Cut | Technical stages: intake 62.9 m → forebay 62.5 → tail 61.55 → weir/Cut-mouth 61.3. Leat is 368.15 m; tail return 557.66 m. The 0.95 m working head can drain; it does **not** establish barge passage. | Act II 454–458 requires the *downstream* dressed tail channel to reach the lower Cut by a wartime spur. Bible 49 also describes barges using the mill route. Current common-outfall graph does not establish that distinct spur or navigability. Inspect a controlled passage/bypass, operating water levels, width/draft and wheel separation before approving works. An upstream-of-wheel bypass would be new detail, not a source-supported replacement for the specified tail connection; no lock is silently added. For now retain drainage evidence and report navigation unresolved. |
| Reedmere under higher water | Existing +1.5 m screen leaves no dry capacity; fen-adapted sites imply roughly 1.13–1.43 m raised floors for the declared 0.3 m clearance. Zone 133 requires stilt huts/plank walks; 139 puts the settlement on the landward edge. | Preserve wet ground, channel conveyance and ridge approaches. Screen candidate floors against locally connected stage + scenario rise + clearance; leave pile bearing, deck links, staging kerb and evacuation access unverified. Do not drain the fen or fill a settlement plateau to turn adaptive capacity into dry-land capacity. |
| Uphill Canal | Current envelope lifts water 61.9 → 80.0 m over 2,432.40 m. The foot's baseline ground is about 68.76 m, while its open-bed proposal is 60.7 m; the cistern's ground is about 77.81 m, below the proposed 80 m surface. This is not yet a modest twenty-step site. | Preserve the alignment and positive head. A local programme must fit foot-pool storage, screened steps, retained cistern, return spill, higher outflow and culvert invert; the map's long stepped line is not a literal construction drawing. Source supply/energy and the detailed correspondence to the small quest space remain unresolved. The dossier hook is anomalous; Discovery 496–500 labels the mechanism proposal/withheld and rejects the ordinary-pump reading. Do not explain it as a pump or pretend downhill gravity solves it. |

For Drowsebank, the fixed centre samples an engineered channel: natural ground is about 67.27 m, open-bed terrain about 60.91 m. A building proxy placed directly on the marker would therefore misleadingly occupy the wheel/race corridor. Real mill footprints, machinery floors and pond banks must be fitted beside the retained waterworks; a sparse foundation test is not a complete mill programme.

## Scope of the local controls

`local_controls.json` references the existing regional inputs instead of duplicating source geometry. Three disjoint, globally aligned 2 m patches cover Crestbridge/Hall/Depot/Mill jointly, Greyharrow and Reedmere. A shared Crestbridge–Mill patch avoids competing overlap edits. Boundaries feather to the regional source; permitted interior changes remain bounded and require composite drainage checks. Cart approaches are tested separately from water-crossing gaps. Sparse foundation pads are feasibility tests, not final plots or architectural generation; Reedmere keeps the stilt/wetland policy.

The bank-refinement control permits up to 1.0 m of local analytic cross-section correction with an 8 m blend to reduce visible 8 m raster imprint. Intermediate generated wet raster samples may change inside the existing corridors; canonical hydraulic junction samples, source water stages and approved XY anchors remain fixed. This is a bounded representation correction, not new geography or additional engineering head, and still requires local/composite drainage verification.

A separate, explicit bed control permits up to 2.0 m of correction only on the existing Drowsebank leat to remove an inherited raster dry dam. The 0.2 m minimum static-depth screen is a defect check, not a discharge, barge-draft or navigation certification; clipped shallow/dry points must remain visible in verification. It changes no source water stage, endpoint or alignment.

The optional Reedmere view uses three existing baseline candidate centres, [416, 2744], [512, 2744] and [440, 2816] m, for neutral 10 × 8 m floor/pile tests only. Each has a finite baseline local water reference; floors use stage + 1.5 m scenario + 0.3 m clearance. The controls fingerprint the source candidate list. These are conditional technical test footprints, not approved building placements, pile designs or a complete connected boardwalk system; no ground grading is permitted for the tests.

**Review: Revise — technical local refinement can proceed, but the compact civic/waterfront relationships and hydraulic operating states are not established.** The next useful Director ruling is the Crestbridge Hall/river/granary arrangement, using the true-scale views. The other five concerns remain explicit decisions or engineering investigations; none is cured by changing a label or passing a downhill graph test.
