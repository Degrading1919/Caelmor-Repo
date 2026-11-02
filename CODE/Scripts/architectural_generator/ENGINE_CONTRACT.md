# Internal implementation contract

Offline Blender tool, original Python geometry, no production game schemas or C#.
Units metres, Z up, footprint CCW. All mesh faces outward.

`model.py`: `Settings(seed=17, function='FARMHOUSE', footprint='L', width=11.0,
depth=7.0, wing_width=4.2, wing_depth=4.5, floors=2, floor_height=2.65,
pitch=48.0, overhang=0.45, detail='HIGH', window_density=1.0)` dataclass,
`make_plan(settings) -> Plan`. `Plan.settings`, `Plan.outline` [(x,y)],
`Plan.rects` rectangles `(x0,y0,x1,y1,axis)` where axis 'X'/'Y' is ridge direction,
`Plan.eave` (0.45+floors*floor_height), `Plan.roof_height(x,y)`,
`Plan.edges` pairs of exterior endpoints, `Plan.rng(label)` stable Random.
Footprints RECT/L/T/U. Main rectangle (0,0,width,depth); wings extend toward negative Y.

`geometry.py`: `MeshBuffer(name, material='timber', layer='structure')` contains
`vertices`, `faces`. `.box(center, size)` closed cuboid; `.beam(a,b,width,depth=None)`
oriented closed cuboid; `.prism(poly_xy,z0,z1)` convex polygon extrusion;
`.extrude(poly_xyz,vector)` convex polygon extrusion; `.cylinder(a,b,radius,segments=8)`.
`.face(points)` adds a polygon. All components closed solids unless stated.
`clip(poly,a,b,c)` returns convex XY polygon satisfying a*x+b*y+c>=0;
`area(poly)`, `lerp(a,b,t)`, `stable_seed(seed,label)`.

`facade.py`: `build_facades(plan) -> list[MeshBuffer]`. Author walls with real depth,
hole subdivisions (no blank wall behind windows), foundation, timber frame avoiding
openings, glazing/lead, shutters, planked door, chimney, details. Group buffers by
material and semantic layer. Legal layers foundation/walls/structure/windows/doors/details.
Plinth 0..0.45. Exterior wall frame follows outline; outward normal (dy,-dx)/length.
Nonenterable exterior only in this release. Root implements roofs, gable infill can
be in facade using roof_height along boundary. Labels material palette:
stone,stone_light,plaster,plaster_patch,timber,timber_light,roof,roof_patch,iron,glass,mortar.

`roof.py`: `build_roof(plan) -> list[MeshBuffer]`, root owner. Clipped analytic
upper envelope of intersecting gables, continuous skin, clipped tile courses,
ridge/valley/flashing and supporting rafters.

`engine.py`: `generate(settings) -> (plan,buffers)`; `validate(plan,buffers) -> dict`
raises ValueError on bad input. `geometry_hash(buffers) -> str`.

`blender_backend.py` agent owner: `build(settings, collection=None, layers=None)`
creates/replaces tagged buffers only in target collection. Shared PBR palette,
UV0 metric projection, UV1 packed lightmap, flat meshes, material tags, custom props.
`export_building(collection, filepath)` glTF + manifest/optional FBX; no claim of Unity validation.
`__init__.py` registration and sidebar UI (Generate New, Regenerate Selected with
layer scope, preserve manual untagged objects). Save settings in collection.
Root package imports bpy lazily so pure unittest imports work outside Blender.

Tests agent owns tests/, evidence render driver, README.md, THIRD_PARTY.md.
Do not publish git from subagents. Do not modify other agents' files.
