# Two architectural benchmarks — 0.8

The Creative Director has not approved 0.7 artistic quality. This pass changes
only LOWMARK/SMITHY and THORNFELL/GATEHOUSE in World mode. The other 78 regional
function combinations and legacy/manual generation remain outside the art pass.
No scene-specific manual modeling, prefab assets, new catalog entries, terrain
system, runtime code or general interior system are introduced.

## Composition before detail

Lowmark Smithy should read as an established agricultural repair workshop with
a dominant timber-framed forge hall, durable hot-work masonry, a substantial
chimney, and a lower attached stock/bench range. Roof hierarchy, enclosure and
thresholds should distinguish it from an open rectangular shed at distance.
Use readable primary bents and actual purlin/rafter bearings, not a dense lattice.
Fire screening, quench, bellows, anvil and a few repair-related working objects
must establish use without filling access with random crates. Practical repairs
and material changes should follow exposure and work, not arbitrary patches.

Thornfell Gatehouse should read as a compact, heavily built pass-control work:
projecting broad flanks shelter a deep entrance; a guard hall bridges the real
passage. Low hipped slate tower roofs and a distinct central roof replace three
repeated tall house-like gables. Stone plinths, battered feet, bonded corners,
proper arched openings, sheltered courtyard access and restrained defensive
apertures express the load paths and climate. Any curtain-wall returns must
suggest an actual boundary, not become an isolated miniature castle or new site.
Do not decorate the building with unrelated banners, weapons or fantasy motifs.

These are reversible art interpretations of the approved regional dossiers:
Lowmark's farming, rebuilding and caravan trade; Thornfell's wind-scoured passes,
stoneworking, ridge forts and reinforced gates. They are not new regional lore,
official material catalogs or real structural/thermal engineering certification.

## Reference boundaries

[Southwater Smithy](https://www.wealddown.co.uk/buildings/smithy-from-southwater/)
is an explicitly **19th-century** vernacular analogue for economical reused
timber, local masonry, fire screening and agricultural repair workflow. It is
not presented as a medieval Caelmor prototype and its design is not copied.
[Dunstanburgh](https://www.english-heritage.org.uk/visit/places/dunstanburgh-castle/history/description/)
supports the distinction between guarded passage, courtyard-accessed guardrooms
and accommodation above; its exceptional scale and exact tower design are not
adopted. Existing archaeological forge guidance remains a process reference.
The new implementation is original and retains the add-on's existing
GPL-3.0-or-later license. No reference assets or implementation code were copied.

## Observable acceptance set

Freeze seed 91, ESTABLISHED, STANDARD, age 35, maintenance .7, MEDIUM/EFFICIENT,
World/grammar on, AUTO context. Preserve the current 0.7 geometry as a baseline
before editing production source. Reuse the existing studio and each native
build across clay/material and multiple cameras. Hold camera/lighting/scale
constant between before and after at each viewing distance, rather than fitting
the improved shape more favorably.

At distance, require a different and purposeful mass/roof hierarchy. At normal
distance, require legible construction, entrances and working frontage. Close
views should confirm real joints, material transitions, usable openings and
selective work equipment. Show opposed whole-building views and useful close
angles; a flattering hero view cannot hide a defective rear or roof junction.
Root review and independent image review may reject an iteration but cannot
grant the Creative Director's final artistic acceptance.

## Technical invariants and validation order

Use cheap two-case generation/validation and deterministic fixture tests during
iteration, then actual Blender body/aperture, roof, stair and forge-air checks.
Arch apertures must cut wall, veneer and collision proxies consistently; the
clear rectangle must fit below the intrados at its lowest point. Check complete
member sections at lean-to/hip roof junctions. Do not fix a failed test by hiding
the offending mesh or narrowing a route below a usable width.

After visual stabilization: test representative seeds/investment/detail modes;
verify the other 78 geometry snapshots; run integration and native regeneration,
protection, export/reopen and package-install gates. Freeze source and bundled
documentation before final captures/packaging. Record image/settings/source and
archive hashes, actual authoring geometry costs and limitations. Model usage,
subscription allowance, tokens, API dollars and wall time remain separate;
do not invent unavailable efficiency measurements.

## Integration findings at source freeze

The new arch-volume test found automatic guard-floor ground supports inside the
passage. Its replacement is a slab borne by the masonry vault. Architectural
review also required real upper doors and supported thresholds from both tower
stair landings into the guard hall; a floor without a connection was insufficient.
Narrow defensive slots initially failed an ordinary-window width threshold and
were silently discarded. They now have explicit aperture semantics and pure/native
air probes through both visible walls and collision proxies. The stock range's
boarded faces use the facade builder so its closed weather faces receive proxies.

The original shed-wall regression is retained as an explicit shed fixture even
though the smithy's primary roof is now gabled. The 78 unaffected geometry hashes
remain regression controls. Final targeted native tests follow the late guard-door
change; the earlier 16-case integration check retains its own source fingerprint.
The six final benchmark tests and both native lifecycle checks passed before
final evidence capture. Technical success does not grant artistic acceptance.

The Luna High evidence worker captured the immutable 24-image control set, then
reported `usage_limit_exceeded`. Root completed implementation, integration and
visual review. No later independent-model art review or model-efficiency advantage
is claimed. Intermediate pilots are developmental evidence; final before/after
records are separately source-pinned and verified.
