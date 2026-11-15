# Lowmark Cottage opening guides

[Editable guide scene](guided-cottage.blend) · [Timber doorway and window](guided-timber.jpg) · [Masonry doorway](guided-masonry.jpg)

The matched-scale Blender views use an 8.40 × 6.25 m box at a 3.35 m wall-head
height and the same elevated camera and lighting. The timber example shows
the shaped lintel, bearing jambs, planked leaf and a side window with a drained
sill. The affluent masonry example shows the same workflow with cut jamb
courses and a radial stone arch. The editable scene captures the timber
example after refitting and leaves the rounded passage open to demonstrate
the separate collision export.

## Construction basis

The timber door interrupts the lower wall member and gives the head full
bearing shoulders. The window sill falls outward and seated side members
carry the head to the storey plate. The curved timber head keeps a straight
top, while the masonry arch divides the same opening profile into radial
stone units on raised jambs. These are Lowmark interpretations of documented
construction principles. See the [National Trust's timber frame survey](https://heritagerecords.nationaltrust.org.uk/HBSMR/MonRecord.aspx?uid=MNA118411)
and [technical examples of shaped timber heads](https://ebrary.net/281224/environment/doorframe_mouldings).

## Checks executed

- Blender 5.0.1 applied a guide to the previously published 0.18 Cottage asset
  without resaving that asset. The native lifecycle test used a rotated box,
  added a door and window, moved and resized the window, and replaced a
  rectangular profile with a rounded face while retaining its guide ID.
- The same test checked finish retention, preservation of unrelated Blender
  objects and staged panel inputs, guide removal, refit, save and reopen, and
  deterministic regeneration. It rejected overlapping guides, an opening too
  close to a corner, and an edit that would replace a protected section.
- Blender ray tests checked a real wall cut behind a closed door and glazing,
  static collision for both, and a collision opening for an open rounded
  doorway. A ray outside the curved crown still hit the visual and collision
  wall. The export kept the approach collider and excluded the source faces.
- The existing blockout lifecycle, construction-library checks and isolated
  extension install passed. The Python generator and construction-library
  suites passed (20 tests). Direct geometry checks also passed for a two-storey
  timber and masonry cottage with a window above the ground floor. A window
  crossing a storey plate was rejected. The synthetic two-volume Roof
  AutoComplete check passed with two valley segments.
- The existing Unity 6000.5.5f1 Editor importer created the open-passage
  prefab under a disposable key. The asset had 36 renderers, 6 colliders,
  13 shared materials, 27 textures and 18,980 imported visual triangles.
  The visual GLB occupied 6.23 MB. Runtime traversal and player behavior
  were outside this check. Adding or removing guides can change the node
  signature, so use a new import key when the existing importer calls for
  one rather than replacing an owned prefab.

Run from the repository root. Set `CAELMOR_OPENING_CHECK_DIR` to a scratch
directory in the checkout to retain the scene and GLBs. Set
`CAELMOR_OPENING_RENDER=1` to also render the two views.

```powershell
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
& $blender -b --factory-startup --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_opening_guides_blender.py
```

## Current limits

This milestone uses the four straight walls of the box-fitted Lowmark
Cottage. Rectangular window and rectangular or symmetric rounded door
profiles are supported. Guidance does not specify arbitrary profiles,
automatic terrain attachment, operable leaves or navigation. Changed
facade buffers are shared across walls within a storey. Hand edits to a
shared buffer should be protected before guide operations.
