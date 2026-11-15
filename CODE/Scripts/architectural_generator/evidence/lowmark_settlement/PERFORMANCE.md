# Lowmark standalone performance baseline

The benchmark imports the saved Farmhouse, Cottage, and Workshop meshes with the Caelmor format-1 sidecars, collision proxies and the existing Unity architecture importer. It uses the showcase's Settlement and Materials camera transforms, the showcase ground geometry with a neutral material and fixed Unity daylight. The Blender ground material blend, dressing, Cycles lighting and optical glass are outside this fixture. This is an asset workload on one laptop and one driver, with no NPCs or simulation load.

## Reproduce

From the designated checkout, run PowerShell 7 with Blender 5.0.1 and Unity 6000.5.5f1 available:

```powershell
./UNITY/Benchmark-Lowmark.ps1
```

The runner exports temporary assets from the tracked showcase, stages the existing runtime, builds separate Windows Development players, then runs them with D3D11. For a repeat on the same inputs pass `-ExportDirectory` with the directory printed by the Blender export marker. Select one player with `-Configuration baseline`, `optimized` or `nomips`. Logs and frames are written to `UNITY/Builds/LowmarkPerformance`. Unity assets are disposable and owned under `UNITY/Assets/__LowmarkPerformance`. The ordinary build and active scene list retain their existing entry points.

To regenerate the aggregate from a complete run, pass the per-player CSVs to the summary script:

```powershell
$fixture = 'CODE/Scripts/architectural_generator/evidence/lowmark_settlement'
$runs = 'UNITY/Builds/LowmarkPerformance'
$frames = 'baseline','optimized','resident','nomips' | ForEach-Object { "$runs/$_-results/frames.csv" }
py -3 "$fixture/summarize_performance.py" @frames --output "$runs/summary.csv"
```

Each case uses a 1920 × 1080 target with v-sync disabled. It warms for 64 frames and records 96 frames at a fixed camera. Counters use Unity's Render profiler category. CPU and GPU timings come from FrameTimingManager when the platform reports a sample. Texture and mesh figures are Unity native memory estimates for resources referenced by the active building variants. The total Unity allocation and global texture counters cover the whole player. All roof variants are loaded by the fixture, so total allocation also includes the inactive variants. [Unity FrameTimingManager](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/FrameTimingManager.html)

The three texture configurations use the same geometry and scene lighting. Baseline uses uncompressed mipmapped textures. Optimized uses BC7 for color and data textures, BC5 for normals, streaming mipmaps, and releases readable CPU copies of visual meshes after setup. Collider assets are separate. A second run of the optimized player disables streaming to isolate residency. No-mips disables the mip chain on uncompressed architecture textures. All these experimental settings live in the fixture.

The scatter uses 217,621 saved transforms and 93 linked specimens. The source distribution has 16,187 LOD0, one LOD1 and 201,433 LOD2 instances, totaling 5,599,658 represented triangles before view culling. The benchmark splits authored spatial tiles by specimen, producing 10,254 possible submissions before culling. It compares full and half density, half density with individual submission, and LOD2 beyond an experimental 18 m cluster-center threshold. The merged submission case culls the same source clusters and packs the surviving transforms into bounded per-specimen draws. All texture configurations compare the showcase with foliage off and with this merged mode. The filled-card control disables alpha rejection and changes depth coverage as well as fragment discard. Interpret this as a workload sensitivity, since it neither counts shaded pixels nor isolates overdraw. Both foliage atlases use a shared benchmark cutout material per atlas, with foliage shadows disabled consistently across cases.

## Import and glass findings

The importer now accepts the specific scale and offset subset of KHR_texture_transform used by the showcase, with positive scales and the appropriate UV origin conversion. Original sampler settings, textures, material identities and Blender source files are retained. The benchmark explicitly drops scalar dielectric specular overrides during GLB staging because the existing Built-in metallic workflow represents them with its standard dielectric response. The conversion records the affected material names and source factors. Texture comparisons use the same conversion on each side.

The glass probe exported 27 closed panes and 682,404 triangles. The GLB contained three material names with double-sided flags and no transmission, volume, IOR or surface maps. The approved Blender thickness, absorption and two-face refraction require a separate real-time material design. All timed settlement cases exclude those panes. Their geometric cost alone warrants a dedicated proxy study with the approved normal and roughness maps before testing refraction. Keep near and distant glass costs separate from the opaque baseline.

The generated 0%, 50% and 100% cases use identical registered bearings and the approved Riven Bake field maps. The Unity scene restores the showcase trim material bindings for each detail variant. The approved showcase itself uses 86%, 95% and 82% for Farmhouse, Cottage and Workshop respectively.

## Standalone measurements

Unity 6000.5.5f1 on Windows, Ryzen 9 270, RTX 5070 Laptop GPU with 7,891 MiB reported VRAM, and D3D11 driver 32.0.16.1742. The four runs produced 3,072 valid measured frames across 32 cases. GPU frame time and aggregate batch and draw counts were unavailable in this player. The standard and instanced draw counters below are the separate Unity Render counters. Triangle counts include render passes and can exceed the number of source triangles.

| Settlement view | Median frame / CPU (ms) | Frame p95 (ms) | Standard / instanced draws | SetPass | Triangles |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full scatter, spatial tile draws | 26.32 / 26.31 | 28.25 | 1,639 / 9,142 | 127 | 12,516,624 |
| Full scatter, merged specimen draws | 13.32 / 13.31 | 15.50 | 533 / 650 | 92 | 12,797,334 |
| Half scatter, spatial tile draws | 20.70 / 20.69 | 22.43 | 2,489 / 8,154 | 128 | 8,352,748 |
| Half scatter, individual draws | 43.34 / 43.33 | 44.97 | 122,131 / 0 | 128 | 8,221,028 |
| Full scatter, experimental distant LOD2 | 26.79 / 26.71 | 31.17 | 1,639 / 9,142 | 127 | 7,095,966 |
| Full scatter, filled-card control | 26.42 / 26.40 | 29.20 | 1,639 / 9,142 | 127 | 12,516,624 |
| Scatter off | 0.64 / 0.63 | 2.55 | 295 / 0 | 78 | 3,696,136 |

Grouping the visible foliage transforms by specimen cut the Settlement median frame interval by 49.4% and reduced the instanced draw counter by 92.9%. The Materials median fell from 8.29 to 4.92 ms. The two captures were byte-identical between the original and merged draw methods at each camera. The wider bounds of each draw slightly increased submitted triangles. The LOD substitution cut wide-view triangles by 43.3% while submission counts stayed fixed and frame times showed no improvement. Filled cards produced similar frame times at both cameras. GPU timings or a fragment workload capture are needed to isolate alpha overdraw. [Full scatter](performance/settlement-full.jpg) · [Merged draws](performance/settlement-merged.jpg) · [Half density](performance/settlement-half.jpg) · [Distant LOD2](performance/settlement-lod.jpg)

| Roof detail | Modeled shingles | Generator roof tris | Imported building tris | Settlement pass-inclusive tris | Materials pass-inclusive tris |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0% | 0 | 6,780 | 149,732 | 3,620,476 | 3,120,100 |
| 50% | 2,087 | 20,566 | 163,518 | 3,679,744 | 3,132,724 |
| 100% | 4,172 | 24,682 | 167,634 | 3,697,452 | 3,136,276 |
| Approved showcase | 3,625 | 24,388 | 167,340 | 3,696,136 | 3,136,260 |

The 0% case reduced wide-view pass-inclusive triangles by 2.1% versus 100%. The foliage-off frame times varied enough across cases that the roof tests established no consistent timing benefit from reducing detail. The close-up captures show the change in roof silhouette and relief. [0%](performance/roof-0.jpg) · [50%](performance/roof-50.jpg) · [100%](performance/roof-100.jpg)

| Building resource settings | Referenced texture estimate (MiB) | Referenced mesh estimate (MiB) | Global texture counter (MiB) | Settlement merged median / p95 (ms) |
| --- | ---: | ---: | ---: | ---: |
| Uncompressed with mips, readable meshes | 608.01 | 58.90 | 516.15 | 13.32 / 15.50 |
| BC7/BC5, resident mips, visual CPU copies released | 152.02 | 29.49 | 161.48 | 13.10 / 14.64 |
| BC7/BC5, streaming mips, visual CPU copies released | 152.02 | 29.49 | 161.48 | 13.15 / 15.00 |
| Uncompressed without mips, readable meshes | 456.01 | 58.90 | 389.48 | 12.99 / 14.56 |

The resource estimates use the foliage-off cases to isolate the building assets. BC compression reduced the referenced texture estimate by 75%. Releasing CPU copies reduced the referenced visual mesh estimate by 50%. The texture streaming run configured 33 textures and showed the same global texture counter as the resident run at the two fixed views. The timing differences between texture configurations were small. The Materials capture changed by a mean of 0.375 RGB levels per channel on an 8-bit scale after compression, with 95% of channel differences at 2 levels or below. The no-mip case shows more high-frequency texture detail competing at distance. A moving camera and target-hardware run would be needed to evaluate shimmer or streaming transitions. [Uncompressed close-up](performance/materials-baseline.jpg) · [Compressed close-up](performance/materials-compressed.jpg) · [No mipmaps](performance/materials-no-mips.jpg)

The three approved building prefabs have 69 renderers and share five of their 13 distinct material assets by reference. The two foliage atlases bring the sequence total to 15. Distinct material finishes retain their own assets. Scene ownership, fixture regeneration, architecture import, saved asset persistence and the existing standalone architecture player all passed after the importer change.

## Priorities

1. Use the measured specimen grouping as the starting point for wider vegetation integration. It has the largest timing benefit and preserves the tested placement and appearance. Keep the implementation in the benchmark until a runtime integration can check moving-camera culling and foliage shadows.
2. Evaluate BC7/BC5 with mipmaps for the Windows player and release CPU data from immutable visual meshes after setup. The measured memory savings justify checking more materials and target GPUs. Keep readable data where code or collision requires it. Keep streaming optional until a moving traversal or a tighter memory budget shows a benefit.
3. Keep approved roof detail and authored vegetation LODs. The experiments reduced triangles without a repeatable frame-time win, and density reductions visibly change ground cover.
4. Profile glass as its own visual compatibility task. Benchmark a simplified real-time pane using shared surface maps and check depth ordering, transparency overlap, and near and far appearance before evaluating refraction. The original optical shader and dense geometry stay in the Blender source.

[Summary CSV](performance/summary.csv) · [Input hashes and export audit](performance/fixture.json) · [Verification log](performance/verification.txt). The same directory contains the four raw frame CSVs and comparison captures.
