# World construction implementation interface

Working coordination document; architectural choices are authored interpretations,
not additions to locked lore. Only this tool directory changes; no agent Git writes.

Root owns `world.py`, model/engine/roof/facade/backend/UI integration. Region owners
write ONLY their assigned new module. Each exports `build(ctx)` and mutates ctx.
No prebuilt meshes. All dimensions in metres. XY outline is counterclockwise.

`ctx.settings`: effective requested Settings with region/context/wealth/function/
craftsmanship/age/maintenance/detail/seed and width/depth/floors/floor_height.
`ctx.mass(key, *, x=0,y=0,width,depth,floors=1,floor_height=None,base=None,
roof='GABLE',pitch=None,overhang=None,openings='DOMESTIC',entrance_edge=0,
blocked_edges=(),steps=True,foundation='PLINTH') -> mass`
Supported roofs GABLE/HIP/SHED/BOW/TERRACE. Each mass is generated parametrically,
with a closed wall body, real apertures, its own roof and structural validation.
Masses have `plan`, `buffers`, `bounds=(xmin,ymin,xmax,ymax)`, `eave`, `base`,
`width`, `depth`, and `roof_height(x,y)` using WORLD coordinates. Mass plans have
facade_records with edge_index/openings/assembly_bounds and world-coordinate edges.
Parts should abut, or be clearly separate, never overlap occupied wall/opening space.
Use blocked_edges on party/abutment facades, move the entrance to an exposed edge.
Core is rectangular; assemble meaningful roofed volumes, not prefab objects.

`ctx.buffer(key, material, layer, zone=mass_or_None) -> MeshBuffer` uses global
coordinates and stores a stable semantic name. Materials familiar stone/stone_light/
timber/timber_light/iron/roof/glass/mortar. Layers foundation/walls/structure/details/
roof/windows/doors. MeshBuffer methods box/prism/beam/cylinder/chamfered_beam.
`ctx.solid_stations(mass, edge_index, spacing=3., radius=.25)` returns stations
along that wall clear of ALL complete opening assemblies across floors.
`ctx.deck(key, polygon_xy, z, thickness=.16, material='timber', zone=None)` -> buffer.
`ctx.stair(key, top=(x,y,z), width, run, direction=(0,-1), material='timber', zone=None)`
builds supported exterior treads/stringers down to grade. Top is outer deck edge.
`ctx.rail(key, a=(x,y), b=(x,y), z, material='timber', zone=None)` makes supported
1m rails; owner must put rails ON real deck and leave doorway/stair gaps.

Root validates each construction zone against its own weather envelope. Exterior
platforms/rails/stairs are explicit supported access geometry, not roof exceptions.
Keep new structural timber details inside the zone roof footprint and under roof.
Stone/iron buttresses can project beyond eaves but must avoid apertures.
Detail LOW/MEDIUM/HIGH controls small geometry, not fundamental identity.
Use ctx.settings wealth/function/context to change real proportions/volumes/access.
All RNG: `ctx.rng(label)` with named deterministic streams; no arbitrary ornaments.

Owners: world_lowmark_thornfell.py (rural service wings vs stepped stone/steep
protected gables); world_mire.py (raised longhouses, bow/reed roofs, supported
decks, stairs, braced piers); world_emberholt.py (TERRACE monumental blocks,
industrial masonry/iron, projecting buttresses, towers/metal walks, NO cottage roof).
