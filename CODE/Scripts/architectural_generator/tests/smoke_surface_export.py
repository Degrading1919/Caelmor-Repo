"""Single legacy FARMHOUSE smoke for the atlas based Blender export path."""
import json
import sys
import tempfile
from pathlib import Path

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from caelmor_architecture.blender_backend import TAG, build, export_building
from caelmor_architecture.materials import PALETTE, SURFACE_REVISION, get_material
from caelmor_architecture.model import Settings
from caelmor_architecture.surface_atlas import ATLAS_REVISION
from test_condition_export import (assert_glb_materials, assert_source_surface_uv,
                                   read_glb, accessor_values)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # A pre-existing manually edited bank entry stays intact. The revisioned
    # material is distinct, cached, and retains a later user shader edit.
    legacy = bpy.data.materials.new("Caelmor | Plaster Patch")
    legacy.use_nodes = True
    legacy["caelm_material"] = "plaster_patch"
    legacy_shader = next(node for node in legacy.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    legacy_color = (.21, .32, .43, 1.0)
    legacy_shader.inputs["Base Color"].default_value = legacy_color
    revision_material = get_material("plaster_patch")
    assert revision_material is not legacy
    assert f"S{SURFACE_REVISION}]" in revision_material.name
    assert all(abs(a-b) < 1e-6 for a, b in zip(legacy_shader.inputs["Base Color"].default_value, legacy_color))
    revised_shader = next(node for node in revision_material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    edited_color = (.31, .41, .51, 1.0)
    revised_shader.inputs["Base Color"].default_value = edited_color
    assert get_material("plaster_patch") is revision_material
    assert all(abs(a-b) < 1e-6 for a, b in zip(revised_shader.inputs["Base Color"].default_value, edited_color))
    revised_shader.inputs["Base Color"].default_value = PALETTE["plaster_patch"][0]
    revision_images = [image for image in bpy.data.images
                       if image.get("caelm_surface_revision") == SURFACE_REVISION]
    assert len(revision_images) == 3
    assert all(image.packed_file is not None for image in revision_images)
    assert all(f"Surface{SURFACE_REVISION}" in image.name for image in revision_images)

    settings = Settings(seed=17, function="FARMHOUSE", footprint="L", detail="LOW")
    collection, _metrics = build(settings)
    meshes = [obj for obj in collection.objects if obj.get(TAG) and obj.type == "MESH"
              and not obj.get("caelm_collider")]
    assert meshes
    atlas_material_names = set()
    neutral_tint_meshes = 0
    source_uv_counts = {"UV0_Metric": 0, "UV1_Lightmap": 0, "UV2_Surface": 0}
    for obj in meshes:
        for name in ("UV0_Metric", "UV1_Lightmap"):
            assert name in obj.data.uv_layers, f"{obj.name} lost legacy {name}"
            uv = np.empty(len(obj.data.uv_layers[name].data) * 2, dtype=np.float32)
            obj.data.uv_layers[name].data.foreach_get("uv", uv)
            assert np.all(np.isfinite(uv))
            assert np.ptp(uv) > 0
            source_uv_counts[name] += len(uv) // 2
        atlas_slots = [slot.material for slot in obj.material_slots if slot.material
                       and slot.material.get("caelm_atlas_revision") == ATLAS_REVISION]
        if atlas_slots:
            assert "UV2_Surface" in obj.data.uv_layers, f"{obj.name} lacks atlas UV2"
            uv = np.empty(len(obj.data.uv_layers["UV2_Surface"].data) * 2, dtype=np.float32)
            obj.data.uv_layers["UV2_Surface"].data.foreach_get("uv", uv)
            assert np.all(np.isfinite(uv)) and np.all((uv >= 0.) & (uv <= 1.))
            source_uv_counts["UV2_Surface"] += len(uv) // 2
            atlas_material_names.update(material.name for material in atlas_slots)
            tint = obj.data.color_attributes.get("CaelmorTint")
            if tint:
                values = np.empty(len(tint.data) * 4, dtype=np.float32)
                tint.data.foreach_get("color", values)
                assert np.all(np.abs(values - 1.) < 1e-6), \
                    f"Atlas-baked condition tint is not neutral on {obj.name}"
                neutral_tint_meshes += 1
    assert atlas_material_names, "Farmhouse has no atlas-bound materials"
    assert neutral_tint_meshes, "No neutral CaelmorTint values checked"

    roof_materials = [material for material in bpy.data.materials
                      if material.get("caelm_atlas_revision") == ATLAS_REVISION
                      and material.get("caelm_material") == "roof_patch"]
    assert roof_materials, "Roof patch atlas material missing"
    roof_base = tuple(roof_materials[0].diffuse_color)
    expected_roof = (.30, .22, .16, 1.0)
    assert all(abs(a-b) < .015 for a, b in zip(roof_base, expected_roof)), (roof_base, expected_roof)

    with tempfile.TemporaryDirectory(prefix="caelmor_surface_smoke_") as tmp:
        glb = Path(tmp) / "farmhouse.glb"
        export_building(collection, str(glb))
        doc, binary = read_glb(glb)
        material_report = assert_glb_materials(doc, binary)
        material_summary = {
            "materials_with_maps": material_report["materials_with_maps"],
            "map_bindings": material_report["map_bindings"],
            "embedded_image_count": material_report["embedded_image_count"],
            "distinct_embedded_png_count": len(set(material_report["embedded_png_sha256"])),
        }
        exported_uv_corners = assert_source_surface_uv(meshes, doc, binary, atlas_material_names)

        # Check any exported vertex colors are normalized. Atlas materials use
        # neutral tint, so an exporter may omit COLOR_0 altogether.
        color_accessors = 0
        normal_accessors = 0
        for mesh in doc.get("meshes", []):
            for primitive in mesh.get("primitives", []):
                attrs = primitive.get("attributes", {})
                if "COLOR_0" in attrs:
                    color_accessors += 1
                    accessor = doc["accessors"][attrs["COLOR_0"]]
                    values = accessor_values(doc, binary, attrs["COLOR_0"])
                    assert accessor.get("normalized", False) or accessor["componentType"] == 5126
                    assert all(-1e-6 <= c <= 1.000001 for sample in values for c in sample)
                    assert all(abs(c - 1.) < 1e-5 for sample in values for c in sample), \
                        "Atlas GLB exported non-neutral legacy vertex tint"
                if "NORMAL" in attrs:
                    normal_accessors += 1
                    values = accessor_values(doc, binary, attrs["NORMAL"])
                    assert all(all(np.isfinite(c) for c in sample) for sample in values)
                    assert all(.985 <= np.linalg.norm(sample) <= 1.015 for sample in values), \
                        "Exported GLB normals are not normalized"
        assert normal_accessors, "GLB contains no normal accessors"
        pbr_factors = [material.get("pbrMetallicRoughness", {}).get("baseColorFactor", [1, 1, 1, 1])
                       for material in doc.get("materials", [])]
        assert all(np.all(np.isfinite(factor)) and all(0. <= c <= 1. for c in factor)
                   for factor in pbr_factors), "GLB material factors are outside normalized [0,1] bounds"
        report = {
            "result": "PASS",
            "fixture": "legacy FARMHOUSE / seed 17 / L footprint / LOW detail",
            "source_mesh_count": len(meshes),
            "legacy_material_preserved": legacy.name,
            "revisioned_material_user_edit_retained": revision_material.name,
            "revisioned_original_bank_images": len(revision_images),
            "atlas_material_count": len(atlas_material_names),
            "roof_patch_palette_rgb": list(roof_base[:3]),
            "source_uv_corner_counts": source_uv_counts,
            "exported_uv2_corner_values_checked": exported_uv_corners,
            "neutral_tint_meshes_checked": neutral_tint_meshes,
            "glb_color_accessors_checked": color_accessors,
            "glb_normal_accessors_checked": normal_accessors,
            "material_export": material_summary,
        }
    evidence = ROOT / "evidence" / "polish_v10" / "legacy_surface_check.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("SURFACE_SMOKE_OK " + json.dumps(report, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
