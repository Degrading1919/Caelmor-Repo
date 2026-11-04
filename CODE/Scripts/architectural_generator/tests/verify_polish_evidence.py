"""Verify capture correspondence and measure GLB payloads for the v10 review."""
import hashlib
import json
import struct
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/polish_v10"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def image(path, digest):
    data = path.read_bytes()
    assert sha(data) == digest, path
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    return struct.unpack_from(">II", data, 16)


def glb_stats(path):
    data = path.read_bytes()
    assert data[:4] == b"glTF"
    length, kind = struct.unpack_from("<I4s", data, 12)
    assert kind == b"JSON"
    doc = json.loads(data[20:20 + length])
    binary_offset = 28 + length
    sizes = {}
    hashes = []
    for i, im in enumerate(doc.get("images", [])):
        view = doc["bufferViews"][im["bufferView"]]
        start = binary_offset + view.get("byteOffset", 0)
        sizes[i] = view["byteLength"]
        hashes.append(sha(data[start:start + sizes[i]]))
    roles = {"base": set(), "normal": set(), "orm": set()}
    for material in doc["materials"]:
        pbr = material.get("pbrMetallicRoughness", {})
        for role, info in (("base", pbr.get("baseColorTexture")),
                           ("normal", material.get("normalTexture")),
                           ("orm", pbr.get("metallicRoughnessTexture"))):
            if info:
                roles[role].add(doc["textures"][info["index"]]["source"])
    return {"bytes": len(data), "images": len(sizes), "image_bytes": sum(sizes.values()),
            "image_bytes_by_role": {role: sum(sizes[i] for i in indices) for role, indices in roles.items()}}, hashes


before, after = (read(OUT / stage / "manifest.json") for stage in ("before", "after"))
assert before["image_count"] == 24 and after["image_count"] == 36
assert after["source_unchanged_during_capture"]
for name, digest in after["generator_sha256"].items():
    assert sha((ROOT / "caelmor_architecture" / name).read_bytes()) == digest, name

frames = {}
for stage, capture in (("before", before), ("after", after)):
    for row in capture["images"]:
        assert image(OUT / stage / row["image"], row["sha256"]) == (1024, 704)
        key = tuple(row[k] for k in ("function", "distance", "finish", "view"))
        if stage == "before":
            frames[key] = row
        else:
            if key[2] == "exported_material":
                key = (*key[:2], "material", key[3])
            for field in ("camera_location", "camera_target", "ortho_scale"):
                assert row[field] == frames[key][field], (key, field)
        if row["distance"] != "close":
            assert row["framing"]["valid"]

sheets = read(OUT / "comparison/manifest.json")["sheets"]
assert len(sheets) == 7
for sheet in sheets:
    assert image(OUT / sheet["image"], sheet["sha256"]) == (sheet["width"], sheet["height"])
    for row in sheet["inputs"]:
        image(OUT / row["image"], row["sha256"])

native = read(OUT / "export_checks.json")
assert native["source_unchanged_during_run"]
mesh_checks = read(OUT / "benchmark_mesh_checks.json")
for report in (native, mesh_checks):
    for name, digest in report["source_sha256"].items():
        assert sha((ROOT / "caelmor_architecture" / name).read_bytes()) == digest, name
assert read(OUT / "legacy_surface_check.json")["result"] == "PASS"
old = ROOT / "evidence/materials_v09"
old_metrics = read(old / "verification.json")["asset_diagnostics"]
measurements = []
for case in after["cases"]:
    function = case["function"]
    key = function.lower()
    old_case = next(c for c in before["cases"] if c["function"] == function)
    assert old_case["settings"] == case["settings"]
    assert sha((old / "final" / f"{key}.blend").read_bytes()) == old_case["input_blend_sha256"]
    assert sha((OUT / "after" / f"{key}.blend").read_bytes()) == case["native_blend_sha256"]
    glb = OUT / "after" / f"{key}.glb"
    assert sha(glb.read_bytes()) == case["export_sha256"]
    new_stats, hashes = glb_stats(glb)
    old_stats, _ = glb_stats(old / f"{key}.glb")
    checked = next(c for c in native["cases"] if c["function"] == function)
    assert checked["geometry_hash"] == case["geometry_hash"]
    native_mesh = next(c for c in mesh_checks["cases"] if c["function"] == function)
    assert native_mesh["source_geometry_hash"] == case["geometry_hash"]
    assert native_mesh["glass_structure_overlaps"] == 0
    assert sorted(hashes) == sorted(checked["material_export"]["embedded_png_sha256"])
    assert old_stats["bytes"] == next(c["glb_bytes"] for c in old_metrics if c["function"] == function)
    measurements.append({"function": function, "before_glb": old_stats, "after_glb": new_stats,
                         "after_geometry": {k: case["validation"][k] for k in ("vertices", "triangles", "objects")}})

archive = ROOT / "dist/caelmor_architecture.zip"
archive_hash = sha(archive.read_bytes())
for key in ("smithy", "gatehouse"):
    report = read(OUT / f"install_{key}.json")
    assert report["archive_sha256"] == archive_hash and report["native_install_and_generate"]
with ZipFile(archive) as package:
    for name in package.namelist():
        source = ROOT / "caelmor_architecture" / name
        assert package.read(name) == (source if source.exists() else ROOT / name).read_bytes()
    members = len(package.namelist())

result = {"valid": True, "revision": after["source_revision"], "matched_native_images": 48,
          "reimport_images": 12, "sheets": len(sheets), "archive_sha256": archive_hash,
          "archive_members": members, "measurements": measurements}
(OUT / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("POLISH_EVIDENCE_VERIFIED", json.dumps(result))
