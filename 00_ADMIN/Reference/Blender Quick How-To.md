# Blender Quick How-To: Turn a 2D Ortho Reference Sheet into a 3D Character Base (Caelmor Shared Rig)

> Goal: build a clean, game-ready **base mesh** that matches your **front/side/back orthographic** sheet, then prep it for the **shared humanoid skeleton** + **attachment sockets** (hands/back/belt/neck).

---

## 0) Fast Checklist (Do This In Order)

1. **Scene setup** (units, scale, naming, collections)
2. **Load reference** (front/side/back) and align to world axes
3. **Blockout** with Mirror (half mesh), correct proportions first
4. **Topology pass** (deform-friendly loops, remove junk)
5. **Socket markers** (empties / bones at neck/back/belt/hands)
6. **Armature fit** (shared skeleton positioned to mesh)
7. **Weights + deformation test**
8. **UVs (if needed)** + export prep (apply transforms, normals)
9. **Export FBX** (Unity-friendly axes)

---

## 1) Scene & Unit Setup (Critical)

### Units / Scale
- **Scene Properties → Units**
  - Unit System: **Metric**
  - Unit Scale: **1.0**
- Target: **1 Blender unit = 1 meter**
- Use the reference height line (ex: **2m**) to scale your image planes.

### Collections (Recommended)
Create collections:
- `REF` (reference images)
- `MESH` (character mesh)
- `RIG` (armature)
- `SOCKETS` (empties / markers)

### Naming (Simple, consistent)
- Mesh: `CH_Base`
- Armature: `CH_Rig`
- Sockets empties: `SOCK_Neck`, `SOCK_Back`, `SOCK_Belt`, `SOCK_Hand_L`, `SOCK_Hand_R`

---

## 2) Bring In the 2D Reference (Ortho Sheet)

### Option A (fast): Image as Plane
1. Enable add-on: **Edit → Preferences → Add-ons → Import-Export: Import Images as Planes**
2. **Shift+A → Image → Images as Planes**
3. Import the sheet, move to `REF` collection.
4. In the image plane material:
   - Disable shadows (optional) / set to shadeless (Emission) for clarity.

### Align to Views
- Put the image plane(s) centered at origin:
  - Front reference: plane faces **+Y** (visible in Front view)
  - Side reference: plane faces **+X** (visible in Right view)
- Separate planes is easiest:
  - Front plane at `Y = -1` (slightly behind the model)
  - Side plane at `X = -1`

### Lock the references (so you don’t bump them)
- Select ref plane(s) → Object Properties
  - Disable **Selectable** in Outliner (filter icon) or
  - Put them in `REF` collection and toggle selection off.

### Scale the reference accurately
1. Add a measurement guide:
   - **Shift+A → Mesh → Cube**
2. Scale cube on Z to **2.0** (if your ref says 2m tall).
3. Scale the reference plane until the character matches that height.

---

## 3) Model the Base Mesh (Mirror Workflow)

### Start: half-mesh + Mirror
1. **Shift+A → Mesh → Cube** (or a single vertex plane)
2. Place at origin; keep symmetry on **X axis**
3. Add **Mirror Modifier**
   - Axis: **X**
   - Enable: **Clipping**
   - Enable: **Merge**

**Rule:** do NOT apply Mirror until the end (unless you must).

### Blockout Pass (10–20 minutes)
- Match **silhouette** in front + side before details:
  - Head size
  - Shoulder width
  - Ribcage depth
  - Pelvis width
  - Arm/leg length
- Use as few polygons as possible.

### Recommended blockout order
1. Torso (ribcage + pelvis volumes)
2. Legs (thigh → knee → calf → ankle → foot)
3. Arms (upper → elbow → forearm → wrist → hand block)
4. Neck + head

---

## 4) Topology Rules for a Game Base

### Deformation loops (must-haves)
- Neck base (1–2 loops)
- Shoulder / deltoid area (clean loops into upper arm)
- Elbow (2–3 loops)
- Wrist (1–2 loops)
- Hip / groin (clean loops into thigh)
- Knee (2–3 loops)
