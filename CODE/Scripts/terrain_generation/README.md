# Lowmark mathematical terrain foundation

Working **offline authoring prototype**, verified against actual elevation arrays
and a full-resolution 3D export. The Director-approved horizontal composition is
kept separate from adjustable metre-scale/elevation assumptions. This is not a
production settlement, runtime terrain generator, hydraulic simulation or locked
world scale. No buildings or NPCs are generated.

## Reproduce

From the designated checkout in PowerShell 7, with Python 3.13 and Blender 5.0.1:

```powershell
./CODE/Scripts/terrain_generation/Generate-Lowmark.ps1 -InstallDependencies
```

Later runs can omit `-InstallDependencies`. Dependencies and application caches
stay in the ignored `.scratch` directory. `-Blender <executable>` selects another
installation; `-SkipMesh` runs array/figure verification without Blender. The
script runs 27 tests, generates the model twice, independently reviews both
terrain states, evaluates scale/resolution/capacity assumptions, renders the
figures, exports the full grid and verifies **every** exported vertex. It uses
batch operations without opening or changing an existing Blender/Unity scene.

Edit [`lowmark_controls.json`](lowmark_controls.json) to adjust authored controls;
do not edit the generated outputs as source. All seven settlement/NPC budgets are
proposed planning targets. Source references and conflicts are documented in
[`SOURCE_NOTES.md`](SOURCE_NOTES.md), with the original mission in
[`MISSION.md`](MISSION.md). Source PNGs are Director-supplied approved project
references; their raw hashes are recorded. Text-source fingerprints normalize
UTF-8/LF so Git line-ending conversion does not invalidate an unchanged source.
No external DEM, geographic dataset, third-party landscape asset or illustration
was used to generate elevations.

## Inspect the result

- [Composition comparison](../../../MEDIA/Maps/Lowmark_Terrain/composition_comparison.png): approved map beside the independently constructed terrain, with the same traced settlement/landmark frame.
- [Hydrology and raster routing](../../../MEDIA/Maps/Lowmark_Terrain/hydrology_and_routing.png).
- [Watersheds and slopes](../../../MEDIA/Maps/Lowmark_Terrain/watersheds_and_slopes.png).
- [Water profiles](../../../MEDIA/Maps/Lowmark_Terrain/water_profiles.png).
- [Orchard floodplain and berm exposure](../../../MEDIA/Maps/Lowmark_Terrain/orchard_floodplain.png).
- [Settlement capacity, slopes and stage exposure](../../../MEDIA/Maps/Lowmark_Terrain/settlement_capacity.png).
- [3D inspection figure](../../../MEDIA/Maps/Lowmark_Terrain/terrain_perspective.png), with explicit vertical exaggeration.
- [Full 8 m terrain GLB](../../../MEDIA/Maps/Lowmark_Terrain/terrain.glb): 480,625 vertices, 958,464 triangles, 23,038,260 bytes; neutral technical material, no finished artwork.
- [Verification](../../../MEDIA/Maps/Lowmark_Terrain/verification.json), [metrics](../../../MEDIA/Maps/Lowmark_Terrain/metrics.json), [mesh verification](../../../MEDIA/Maps/Lowmark_Terrain/mesh_verification.json).
- [Executed milestone test/export log](../../../MEDIA/Maps/Lowmark_Terrain/execution.txt).

`height.npy` is the conditioned natural/gated baseline. `height_engineered.npy`
is the combined open-bed design used by the GLB. Both are metric float32 arrays;
the NPZ retains float64 fields, flow receivers and accumulation for inspection.
Arrays start at the southwest corner, rows increase north, columns east. Blender
uses east X/north Y/elevation Z; GLB uses east X/elevation Y/minus north Z. A later
engine-specific adapter must apply a consistent world basis to terrain and props.
The existing architectural building importer is **not** a terrain importer and
has not been changed.

Executed on Python 3.13.15 / NumPy 2.3.4 / PowerShell 7.6.9 / Blender 5.0.1
(`a3db93c5b259`). The 27 tests took about 9.24 s; one regional generation took
8.41 s. Generation, independent checks, repeat generation and scale/resolution
studies took 75.91 s before figure rendering. These are observed wall times,
not runtime frame-rate measurements. The saved GLB's maximum vertical deviation
from all 480,625 float64 samples is 0.00000763 m.

`height.png` is a calibrated 16-bit export; `terrain.obj` is a **32 m display
preview**. Neither is the hydrological authority. Quantization is about 2.64 mm
and introduces flat/terminal cells under strict dry-bed D8 routing (the exact
count is recorded in `verification.json`). Preserve
the float arrays/full-resolution GLB and revalidate any tiled, quantized or
resampled production representation. A future Unity Terrain import will need its
own tile/resolution/flat-routing treatment; no Unity integration is claimed here.

## Method and mathematical boundaries

1. **Local coordinate frame.** The map panel is traced in normalized east/north
   coordinates, retaining original pixels. Working extent is 6,144 × 4,992 m,
   sampled at 8 m: 769 × 625 samples, 30.670848 km². Illustrated elevation bands,
   contour intervals and the scale bar are not sampled as measurements.
2. **Authored regional field.** An affine trend plus smooth Gaussian radial
   landform controls creates uplands and broad terrain. River valleys, a fen
   basin/fringe and a broad lowland along the retained Cut alignment are explicit
   constraints. The fen uses nearest-channel stage, low-amplitude analytic relief
   and a blended shore apron; it is not a uniformly submerged polygon or a
   flattened settlement pad. There are no unconstrained noise octaves. The saved
   seed is provenance; the current solver has no random terms.
3. **Drainage skeleton.** Each natural reach has an authored polyline and strictly
   descending metric bed profile. Junction levels are shared. Projection onto a
   reach gives station and cross-channel distance; a bounded cross-section and
   valley envelope shape the land. The eight-neighbour raster graph is checked
   for alias cycles; tiny local raster backtracks can be reconciled within the
   declared channel envelope without moving authored coordinates. At 8 m, maximum
   recorded raster deviation is about 8.8 m. At 16/32 m the current network merges
   incompatible junctions and is correctly rejected, rather than declared valid.
   Bank lower bounds act in finite, smoothly blended per-reach corridors after
   regional wetland/floodplain shaping and before drainage conditioning. This
   order prevents a later apron pass from erasing headwater containment. A
   globally nearest high-channel floor was rejected during 3D review because it
   created a distant Voronoi escarpment. The fen's upstream guard likewise uses
   the declared Falls direction and a smooth boundary fade, rather than a hard
   nearest-channel classification. Continuity tests retain the actual waterfall
   while rejecting pathological elevation steps away from it.
4. **Constrained conditioning.** A priority queue propagates from immutable
   channel cells, raising otherwise trapped terrain only as needed, with a 1 mm
   increment. This is a constructed terrain solution, not proof that an arbitrary
   initial landscape was natural. The final model conditions 4.67% of samples,
   maximum 9.41 m; the 95th-percentile raise is zero. A smooth 25 m / 350 m-radius
   northwest boundary-rim proposal keeps the formerly trapped corner within the
   unchanged 12 m repair budget. The remaining frame edges are closed in this
   single-outlet study; the actual off-map divide is unsurveyed. These synthesis changes are
   not historical human earthworks. The approach draws on
   [Barnes, Lehman & Mulla, Priority-Flood (2014), DOI 10.1016/j.cageo.2013.04.024](https://rbarnes.org/sci/2014_depressions.pdf);
   the prototype is original Caelmor code and uses authored channels as seeds.
5. **Independent verification.** A separate implementation recomputes actual
   steepest downhill receivers, using diagonal distance `sqrt(2) × cell size`,
   verifies adjacency/strict descent, and conserves all contributing samples to
   the declared outlet. Model-derived subcatchments additionally use 64/32/16 m²
   interior/edge/corner weights, conserving the exact rectangular area. Negative
   tests reject dammed terrain, fabricated receiver jumps, hidden interior
   outlets and false accumulation. Both natural and combined open-bed DEMs pass.
6. **Engineered water.** Separate bed/water profiles represent Hollow Lock, the
   Cut, mill race, Bramblelock and canal. Current static heads are 1.1 m at Hollow
   Lock, 1.2 m at Bramblelock and 0.95 m at the mill. Common 1.2 m planning depths
   avoid an unmodeled outfall sump; they do not certify navigation/draft. An early
   background implied a 19.7 m Cut excavation; a revised broad lowland constraint,
   keeping the same alignment, reduces the actual maximum to about 5.7 m. This is
   still substantial work needing local bank/structure design. Backwater
   reconstruction, passive excavation and anomalous-canal geometry are reported
   separately; overlapping corridor volumes must not be summed.

The orchard is a separate agricultural constraint, not a settlement pad. Its
0.467 km² field polygon has ground at 61.81–63.29 m against a 61.3 m reference
stage. Normal connected inundation is zero; the connected +1.5 m scenario reaches
22.2% of the field while 87.2% of the proposed berm area remains outside it.
The broad local drainage apron is an explicit technical inference along the
existing Cut-mouth/towpath works, not a newly approved major river. The initial
field at roughly 7.7 m above water failed the floodplain check and was rejected.
No trees, field parcels or completed dikes/sluices are generated.

The 2.821 km² fen has shallow reference channels and low emergent ground: 4.84%
of its samples are water-covered at the normal stage, with median/p95 slopes
0.109°/3.106°. This is a normal-stage geometry scenario; groundwater, seasonal
saturation and smaller marsh channels need local refinement.

D8 is a **topographic routing surrogate**, not a discharge, groundwater,
sedimentation, flood-frequency or gate-cycle solution. Actual shallow-water
hydraulics depend on water-surface gradients and conservation of volume/momentum,
not just downhill bed samples; see the
[USACE shallow-water equations](https://www.hec.usace.army.mil/confluence/hecras/beta/technical-reference/hydraulic-equations/shallow-water-equations).
Locks also need a water supply and operating water budget; see the
[Canal & River Trust operational explanation](https://canalrivertrust.org.uk/our-cause/looking-after-canals-and-rivers/managing-our-water/day-to-day).
The supplied PNGs are retained unchanged as planning references; their illustrated
contour pixels are not sampled into elevations. No scientific paper text or
third-party implementation code was copied. Pinned NumPy/Matplotlib/Pillow
dependencies remain external packages under their bundled licenses.

## Scale and capacity findings

The 4.096 × 3.328 km trial (4 m grid) compresses slopes and loses Ashenstead/Greyharrow
capacity under the retained vertical/landform assumptions. This is a model result,
not proof that every smaller-world design is impossible. The 8.192 × 6.656 km
trial increases spacing and some capacity, but costs traversal and content density.
The middle extent is a **working compromise for review**, not approved world size.
At the technical fixture's 3 m/s walk / 5.5 m/s sprint, a straight east-west crossing
is 34.1 / 18.6 minutes; those speeds are sensitivity inputs, not locked balance.
Route lengths, ground grades and crossings are in `verification.json`.

Capacity uses actual combined terrain, conservative spaced footprint checks,
declared mean roof area/plot coverage, road/public-space reservations, slope and
freeboard thresholds. Waterworks are excluded. No settlement grading is performed.
The envelope uses the **upper proposed span**; smaller spans often cannot support
even the lower proposed building count under these assumptions.

| Settlement | Proposed roofs | Normal-stage screen | Outside connected +1.5 m exposure screen | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Brookhollow | 75–120 | 145 | 134 | Larger end of the 400–650 m span needed; 400 m screen holds only 61. Low waterfront remains distinct from upper ground. |
| Crestbridge | 60–100 | 97 | 91 | Supports most of range at 600 m; 350 m screen only 28. Hall/Depot are separate outworks, not silently compressed into the town. |
| Ashenstead | 35–60 | 78 | 78 | 420 m village envelope works; 220 m screen only 22. Extensive surrounding fields remain outside the core. |
| Greyharrow | 28–50 | 23 | 18 | Conservative baseline shortfall. A 120 m² mean roof/40% plot coverage/5° site sensitivity yields about 44/37 without terrain changes; 50 is not established. |
| Reedmere | 12–24 | 43 | 0 | Fen adaptation is necessary for the +1.5 m scenario. Candidate centres imply roughly 1.13–1.43 m raised floors for 0.3 m clearance; no piles or drainage works generated. |
| Whisperflow Landing | 5–12 | 19 | 19 | Small worksite fits; no large plateau. |
| Drowsebank Mill | 4–10 | 4 | 4 | Leat and access reduce baseline to lower end. A 120 m²/40%/5° sensitivity fits 9; 10 is not established. Engineering/wheel layout is not built. |

These are planning screens, not promised final building counts or flood-safety
certification. The +1.5 m scenario uses elevation-connected susceptibility;
isolated low pockets are not automatically treated as flooded. NPC figures
remain recorded planning estimates; no characters or simulations are created.

## Review before production lock

- **Western Whisperflow arm:** the illustration appears to end near the landing.
  Current geometry treats it as a connected side backwater and marks topology
  unresolved. A continuous main-channel return must be confirmed, not invented.
- **Uphill Canal:** the regional envelope rises 18.1 m over about 2.43 km. The
  existing anomalous hook is preserved; its energy/source mechanism is not
  explained as an ordinary pump or fake downhill flow. The local twenty-step
  quest space and cistern need a separate site design; the drawn regional steps
  are not literal metre-scale construction drawings.
- **Fen closure:** an older quest says closing the Cut leaves no outlet, despite
  the approved natural main-river outlet. That quest-state hydraulic contradiction
  remains explicit; the prototype does not silently dam or remove the main river.
- **Access/pacing:** bridge/culvert crossings remain unbuilt. The direct Falls
  approach intersects the steep fall site and is not a walkable finished path;
  local listening-step/switchback access must be fitted within its retained
  location. Part of Crestbridge–Ashenstead exceeds the conservative cart-grade
  screen away from water crossings. Long regional journeys cannot inherit old
  60–90 second quest-transition assumptions. No quest/runtime text was rewritten.
- **Steep terrain and resampling:** maximum neighbouring height differences
  outside 200 m of the Falls are 11.80 m on natural terrain and 14.12 m on open
  engineered terrain. These pass the regression that rejects the former 136 m
  discontinuity; they do not establish walkable slopes or finished canal banks.
  The upland fen fringe and engineered banks need local sections and finer tiles.
- **Outworks and capacity:** Hall is about 648 m and Depot 779 m from Crestbridge's
  core anchor, outside a 600 m built-up core. Confirm whether the proposed span
  includes outworks; retain their approved positions. Greyharrow density, mill
  ancillary space and fen platform design need local site programmes.

**Milestone: Pass — working deterministic mathematical foundation; review/local
refinement required before production terrain or settlement assembly is locked.**
Next: Director review of the flagged topology/scale/site assumptions, then 1–2 m
local terrain and engineering tiles for the Falls approach, Greyharrow, mill and
waterworks. Preserve the regional controls, validate resampling/tile seams, and
only then prepare a terrain-specific Unity authoring handoff.
