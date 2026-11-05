# Architectural asset pipeline

This offline Editor workflow prepares existing Caelmor generator exports for later
hand placement. It creates no settlement, occupancy areas, navigation links, or
automatic floor-hiding integration. The generator's existing
[`CaelmorBuildingExport` format 1](../CODE/Scripts/architectural_generator/ENGINE_CONTRACT.md)
remains the input contract.

## Ownership and safe scene work

`PlayableFoundation.unity`, `PlayableNavigation.asset`, the six technical fixture
materials listed in `PlayableFixtureOwnership.txt`, and their GUIDs are reserved
generated fixture resources. Use a separate saved scene for Creative Director
world layouts. The importer does not open or save world scenes.

Standard builds consume saved enabled Build Settings scenes. They no longer call
`CreateScene`, rebake navigation, replace a scene, or reset the build list.
Technical validation temporarily opens the existing fixture in isolation and
restores the prior scene setup without saving its temporary changes. Unsaved scene
work and Prefab Mode block operations that would switch scenes. Fixture generation
is an explicit `Caelmor > Technical fixture > Regenerate owned playable scene`
operation; changed fixture resources or GUIDs cause a conflict before replacement.
Preserve deliberate fixture edits elsewhere or reconcile them explicitly before
regenerating. Ownership records are generated tool evidence, not a way to approve
unknown work by overwriting hashes.

## Import the next building

Export **GLB** from the existing generator. Keep the matching `.caelmor.json` and
the sidecar-declared collision GLB beside it, inside this checkout. From the
repository root in PowerShell 7:

```powershell
./UNITY/Import-Architecture.ps1 -Source './CODE/Scripts/architectural_generator/evidence/benchmarks_v08/gatehouse.glb' -Key 'thornfell_gatehouse'
```

Choose the key once and reuse it for updates. A changed key creates another asset
identity. Keep Blender object/buffer names and the section hierarchy stable for
updates to assets already placed in scenes. The import command stages the existing
runtime DLL and launches the licensed Unity 6000.5.5f1 Editor in batch mode. Logs
stay in `UNITY/Logs`; builds stay in `UNITY/Builds`. Unity Package Manager resolves
the pinned dependencies on first use. No Blender installation is required to
import an already exported GLB.

For a new export, replace the source path and select a new stable key. Close the
Unity Editor before running a batch command against this project. The saved
floor-separated verification building also has explicit material bindings:

```powershell
./UNITY/Import-Architecture.ps1 -Source './CODE/Scripts/architectural_generator/dist/floor_visibility_demo.glb' -Key 'floor_visibility_demo' -Bindings 'Assets/_Project/World/Architecture/Bindings/floor_visibility_demo.asset'
```

Place `Assets/_Project/World/Architecture/Prefabs/<key>.prefab` in an authored
scene. This artist-owned prefab variant inherits the generated source at
`Architecture/Generated/<key>/<key>.prefab`. Keep artist additions, material
replacements, and intentional section overrides in the variant or scene instance.
Shared meshes, textures, and materials are referenced across instances. The source
sidecar remains available at `Generated/<key>/source.caelmor.json`; node identity
components retain construction and optional floor metadata without occupancy.

An identical import is a no-op. An update with compatible identity and hierarchy
updates generated source assets while preserving placement prefab GUIDs and
overrides. Changed hierarchy/section contracts, changed binding configuration,
missing placement GUIDs, generated-resource edits, and unsupported material
features fail before publication. Reconcile those conflicts deliberately or use a
new asset key and review placements. Import errors roll back touched generated
files; this does not provide crash/power-loss transactional guarantees. Do not
hand-edit generated source files or their ownership ledger.

## Material boundaries

The existing generator atlas and the painting library are distinct material
systems. A generator key such as `roof` is insufficient to select a painting
library material or establish its repeat scale. Unbound sections retain their
exported PBR materials and are reported as unresolved library mappings.

The packaged floor demonstration uses UV0 metric, UV1 lightmap, UV2 surface atlas,
and UV3 detail normal coordinates. glTFast preserves those mesh channels but its
built-in material shader accepts only UV0/1. The Caelmor PBR adapter selects the
original UV channels independently, retains vertex color, factors and ORM
channels, and prepares tangents from the selected normal UV. The derivative GLB
normalizes only temporary importer material UV declarations; original source GLB
and sidecar stay unchanged. glTFast decodes geometry and instantiates the hierarchy.

Two original grayscale baselines, `split_oak_shingle` and `forged_iron`, are staged
for explicit verification bindings. Their master textures are read only. Color is
sRGB; roughness, metallic and normal maps are linear. The staging helper records
the catalog ID, physical U/V repeat, original package SHA-256 and every generated
map hash. Artist-edited staged maps cause a conflict; stage a deliberate new
resource rather than overwriting an edit.

The optional preparation command requires Python 3 and Pillow:

```powershell
py -3 UNITY/Tools/stage_material_library.py --id split_oak_shingle --id forged_iron
```

Do not replace atlas UVs with painting-template UVs. A library binding requires an
explicit assertion that the source UV0 is metric and has the intended course/grain
orientation. The catalog repeat dimensions divide that metric UV. Hand painting,
palette/overlay baking in Blender, and deliberate selection of a surface remain
artist steps. The entire 100-material master library is unchanged.

Create optional bindings with `Assets > Create > Caelmor > Architecture material
bindings`. Set each entry's `bufferId` to the exact sidecar `objects[].name`, select
an existing staged library `materialId`, and assert verified metric UV0. Pass that
asset path using `-Bindings`. The verification binding makes two deliberate
technical assignments; it is not an automatic mapping policy for every roof or
metal surface.

For painted production returns, use the existing material-library return-to-Blender
procedure, resolve palette/overlay nodes to standard glTF PBR images, assign the
intended finish, and export the building again. Alternatively create an
artist-owned Unity material/texture resource and override the placement variant.
Keep such resources outside generated/shared/staged-baseline ownership. A direct
edit to a generated resource intentionally blocks import until reconciled; the
baseline stager is not a painting-return or global material-migration tool.

Current support is static triangle GLB 2.0 with embedded PNG/JPEG images, opaque or
masked metallic/roughness PBR, original UV0 through UV3 and known linear/trilinear
samplers. Transparent/emissive materials, extensions such as texture transforms,
animation/skins, and unsupported sampler/occlusion-UV combinations are rejected.
Export the generator's GLB option; separate `.gltf` input is not implemented.
Collision proxies become separate static non-convex MeshColliders. Their source
approximation and traversal limits remain; import does not bake a world NavMesh.

## Dependencies and rights

The importer uses official Unity glTFast **6.14.1** (Apache-2.0), package revision
`20fc683570b1c3d52511255324b8c02f12e1524e`, fingerprint
`0847aee0f6da9f7f63ea95a8a3ea4906dba73079`. Newtonsoft JSON **3.2.1** provides
bounded GLB JSON-container inspection and normalization; glTFast decodes meshes.
The Unity Newtonsoft wrapper revision is
`d8e49aef8979bef617144382052ec2f479645eaf`, fingerprint
`74deb55db2a0c29ddfda576608bcb86abbd13ee6`; its wrapper uses the Unity Companion
License and Newtonsoft.Json 13.0.2 has its bundled upstream notices. These are
Unity project dependencies, used under their package licenses.
The checked Package Manager lock records transitive versions. Packages remain
Package Manager dependencies; their source is not copied into this repository.
Original Caelmor building geometry and material baselines are the only test assets.

References: [Unity glTFast project setup](https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.14/manual/ProjectSetup.html),
[glTF 2.0 coordinate, UV and PBR contract](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html),
and [Caelmor material handoff](../MEDIA/Materials/README.md).

## Executed verification and cost

Fixture inputs are the existing generator exports from verified main `35c02db`:
the packaged Lowmark floor-separated demonstration (generator 0.16.0) and the
structurally distinct Thornfell gatehouse benchmark (0.8.0, legacy unsplit format 1).
Their geometry and material images are original Caelmor outputs. The legacy
building lacks a persistent floor-presentation building ID, so its explicit stable
asset key supplies `asset:thornfell_gatehouse`; the newer fixture retains its
exported building ID. Unity applies the glTF right-to-left-handed X reflection;
metres and local Y height remain unchanged.

| Fixture | Visual meshes / renderers | Collision meshes | Assigned materials | Referenced textures | Triangles | Source bundle bytes | Generated owned bytes | First import |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Floor-separated demo | 79 | 15 | 13 | 31 | 61,262 | 17,678,458 | 50,708,241 | 7.79 s |
| Thornfell gatehouse | 149 | 15 | 10 | 9 | 42,006 | 5,075,515 | 19,747,903 | 6.51 s |

Source bundle size includes GLB, collision GLB and sidecar. Owned generated sizes
include shared resources and metadata and must not be summed as a unique storage
budget. Initial measured unique pipeline storage is **340 asset files / 70,828,942
bytes**, including `.meta` bytes but excluding `.meta` from file count and excluding
Unity's Library cache/subassets. Multiple scene instances share these resources.
Timings exclude package resolution, Editor startup and runtime DLL staging; they
are local observations, not cross-machine performance guarantees.

Unity reported unique referenced texture/native visual mesh estimates of
**96,302,767 / 22,428,768 bytes** for the floor demo and **664,287 / 13,311,104 bytes**
for the gatehouse. These are Editor native-resource estimates, not player RSS or
GPU measurements. The floor demo's high-resolution per-building atlases dominate
its cost; sharing across instances does not eliminate per-building atlas variety.
The Editor also retains 21 unused source-material subassets in the imported GLBs,
alongside the 23 native assigned material assets. Generated prefabs reference the
native prepared meshes/materials and external shared textures.

This fidelity baseline uses uncompressed imported textures, mipmaps, readable
prepared meshes, and separate semantic renderers. Source GLB derivatives retain
unused embedded image payloads as well as referencing extracted shared images;
this increases Editor disk storage without making another material/texture per
placed instance. Content-hashed shared images and materials retain distinct
sampler/color roles and PBR definitions. Old referenced resources are not purged
automatically. This pipeline does not establish a settlement draw-call, streaming,
LOD, GPU-time or memory budget.

The glTFast package itself occupied 6.13 MiB in the local cache; required Burst
1.8.29 occupied 850.97 MiB, Newtonsoft 6.84 MiB and Collections 5.34 MiB. These are
Editor/dependency disk costs, not per-building or per-instance player costs. The
official importer was selected to avoid maintaining a mesh/scene decoder; the
additional PBR adapter handles the actual four-UV Caelmor exports.

Run the complete asset/scene suite and fresh-Editor persistence checks with:

```powershell
./UNITY/Import-Architecture.ps1 -Validate
```

This also builds a disposable Windows player containing two floor-demo instances
and one gatehouse, then runs native collision and shared-resource checks. The
Editor operations use `-batchmode -nographics`. The player uses hidden,
non-interactive `-batchmode -force-d3d11`: a real Direct3D 11 device is required for
runtime custom-shader property inspection. Unity's Null graphics device did not
expose those properties. This does not involve desktop automation or a playtest.

Executed results: **13,101 import assertions**, **13,075 fresh-Editor persistence
assertions**, scene-ownership checks, **105 runtime regressions**, two material
staging tests, source compilation with zero warnings/errors, Windows shader/player
compilation, native player checks for **307 renderers / 45 colliders / two shared
floor-building instances**, and the existing technical standalone smoke. All
100 master textures, the original technical scene and original navigation asset
matched their pre-work SHA-256 values. Accepted machine-readable measurements are
in [ArchitectureValidationEvidence.json](Tools/ArchitectureValidationEvidence.json).

The suite reads independent position/UV samples from the original GLBs, verifies
section identities/hierarchy, metre scale/orientation, original material factors,
normal channels/tangents, physical library repeats, collision separation, shared
instances, no-op reimport, changed-source reimport, authored additions/material
overrides after saved-scene reload, and failed-import rollback/retry. It refuses
pre-existing reserved test paths. The scene suite also executes explicit fixture
generation while preserving saved authored scenes, terrain, artist materials,
build lists and original fixture bytes. The original technical build and its
standalone gameplay regressions remain a separate compatibility check:

```powershell
./CODE/Build-And-Validate.ps1 -Configuration Release
./UNITY/Build.ps1
./UNITY/Tools/Compile-Source.ps1
```

Run an Editor import/build before the standalone source check on a fresh checkout;
the source check references the pinned Newtonsoft DLL from Package Manager's
resolved cache. The architecture verification player build measured 211,639,078
bytes including Unity runtime files; its final incremental build took 3.31 seconds
(the initial build took 18.99 seconds). These are validation-build measurements.

Generated logs and machine-readable measurements stay in `UNITY/Logs`; accepted
measurements are recorded here and in the import records. Compilation, asset
validation and native physics checks do not substitute for artistic acceptance.
No interactive gameplay or Computer Use was performed. Final material appearance,
hand-painted returns, building-specific collision/traversal review, authored
occupancy, lightmaps and approved world placement remain manual production steps.
The prefab and scene-ownership workflow supports later Creative Director-authored
settlement assembly without rebuilding model hierarchies by hand.
