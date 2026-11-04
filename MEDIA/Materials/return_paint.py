#!/usr/bin/env python3
"""Safe, revisioned Procreate texture return and Blender material handoff.

Package contract: master.png, color.png, roughness.png, metallic.png,
normal.png, height.png (any subset after master/color is allowed). Optional
overlay.png is a separate, reusable layer; palettes are reusable JSON stops. A package
may be a directory or ZIP; PNG files are sRGB for color/overlay and
linear data for the scalar/normal maps. Run `--help` outside Blender. Blender
API: build_blender_material(package, material_name=None, scale_m=None,
object=None, slot_index=None, replace_slot=False).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import sys
import tempfile
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

MAPS = {"master", "color", "roughness", "metallic", "normal", "height", "overlay"}
GRAY_MAPS = {"master", "roughness", "metallic", "height"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_extract(zf: zipfile.ZipFile, dest: Path) -> Path:
    root = dest.resolve()
    for info in zf.infolist():
        name = PurePosixPath(info.filename)
        if name.is_absolute() or ".." in name.parts:
            raise ValueError(f"Unsafe ZIP path: {info.filename}")
        target = (dest / Path(*name.parts)).resolve()
        if target != root and root not in target.parents:
            raise ValueError(f"Unsafe ZIP path: {info.filename}")
    zf.extractall(dest)
    children = [p for p in dest.iterdir() if p.is_dir()]
    return children[0] if len(children) == 1 and not any(dest.glob("*.png")) else dest


def _package_root(path: Path, temp: tempfile.TemporaryDirectory | None = None) -> Path:
    if path.is_dir():
        return path
    if path.is_file() and zipfile.is_zipfile(path):
        if temp is None:
            raise ValueError("Internal error: ZIP extraction requires a temporary directory")
        with zipfile.ZipFile(path) as zf:
            return _safe_extract(zf, Path(temp.name))
    raise ValueError(f"Package must be a folder or ZIP: {path}")


def _png(path: Path):
    """Decode common 8-bit Procreate PNG modes using only the Python stdlib."""
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Expected PNG: {path}")
    pos, chunks, width, height, depth, ctype = 8, [], None, None, None, None
    while pos + 12 <= len(raw):
        length = struct.unpack(">I", raw[pos:pos+4])[0]
        kind = raw[pos+4:pos+8]
        data = raw[pos+8:pos+8+length]
        if len(data) != length: raise ValueError(f"Truncated PNG: {path}")
        if kind == b"IHDR": width, height, depth, ctype, comp, filt, interlace = struct.unpack(">IIBBBBB", data)
        elif kind == b"IDAT": chunks.append(data)
        elif kind == b"IEND": break
        pos += length + 12
    if not width or width != height:
        raise ValueError(f"Texture must be square: {path} ({width}x{height})")
    if depth != 8 or ctype not in (0, 2, 4, 6) or comp != 0 or filt != 0 or interlace != 0:
        raise ValueError(f"Unsupported PNG encoding (need non-interlaced 8-bit grayscale/RGB/RGBA): {path}")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[ctype]
    try: decoded = zlib.decompress(b"".join(chunks))
    except zlib.error as e: raise ValueError(f"Invalid PNG data: {path}: {e}") from e
    stride, bpp = width * channels, channels
    expected = height * (stride + 1)
    if len(decoded) != expected: raise ValueError(f"Invalid PNG pixel data size: {path}")
    rows, offset, prior = [], 0, bytearray(stride)
    for _ in range(height):
        method = decoded[offset]; offset += 1
        scan = bytearray(decoded[offset:offset+stride]); offset += stride
        if method not in range(5): raise ValueError(f"Invalid PNG filter: {path}")
        for i in range(stride):
            a = scan[i-bpp] if i >= bpp else 0
            b = prior[i]
            c = prior[i-bpp] if i >= bpp else 0
            if method == 1: scan[i] = (scan[i] + a) & 255
            elif method == 2: scan[i] = (scan[i] + b) & 255
            elif method == 3: scan[i] = (scan[i] + ((a+b)//2)) & 255
            elif method == 4:
                p = a+b-c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                predictor = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                scan[i] = (scan[i] + predictor) & 255
        rows.append(bytes(scan)); prior = scan
    mode = {0: "L", 2: "RGB", 4: "LA", 6: "RGBA"}[ctype]
    return (width, height), mode, rows, channels


def _image_info(path: Path):
    size, mode, _, _ = _png(path)
    return size, mode


def _is_grayscale(path: Path) -> bool:
    _, mode, rows, channels = _png(path)
    if mode in ("L", "LA"): return True
    rgb_channels = 3
    return all(row[i] == row[i+1] == row[i+2]
               for row in rows for i in range(0, len(row), channels))


def parse_mapping(value: str) -> tuple[str, Path]:
    key, sep, val = value.partition("=")
    key = key.strip().lower()
    if not sep or key not in MAPS or not val.strip():
        raise argparse.ArgumentTypeError("Use MAP=PNG where MAP is " + ", ".join(sorted(MAPS)))
    return key, Path(val.strip()).expanduser().resolve()


def _catalog_rows(data):
    rows = data.get("materials", []) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("catalog.json must be an array or an object with a materials array")
    return rows


def _srgb_linear(value):
    value = int(value, 16) / 255.0
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def return_paint(package: Path, imports: list[tuple[str, Path]], output: Path,
                 package_id: str | None = None, catalog: Path | None = None) -> Path:
    """Create a new revision package; never mutate the input package or sources."""
    package, output = package.expanduser().resolve(), output.expanduser().resolve()
    if not imports:
        raise ValueError("Select at least one mapping with --import-map MAP=PNG")
    keys = [k for k, _ in imports]
    if len(keys) != len(set(keys)):
        raise ValueError("A mapping may be imported only once per revision")
    with tempfile.TemporaryDirectory(prefix="caelmor-paint-", dir=Path(__file__).resolve().parent) as td:
        temp = tempfile.TemporaryDirectory(prefix="caelmor-package-", dir=Path(__file__).resolve().parent) if package.is_file() else None
        try:
            root = _package_root(package, temp)
            metadata = root / "metadata.json"
            source_id = json.loads(metadata.read_text(encoding="utf-8")).get("id") if metadata.exists() else None
            if package_id and source_id and package_id != source_id:
                raise ValueError(f"Requested ID {package_id!r} conflicts with package ID {source_id!r}")
            pid = source_id or package_id or root.name
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", pid):
                raise ValueError(f"Unsafe package id: {pid}")
            catalog_row = None
            if catalog:
                rows = _catalog_rows(json.loads(catalog.read_text(encoding="utf-8")))
                catalog_row = next((r for r in rows if r.get("id") == pid), None)
                if catalog_row is None:
                    raise ValueError(f"Package id {pid!r} is not in {catalog}")
            sizes = {_image_info(p)[0] for p in root.glob("*.png")}
            if len(sizes) > 1:
                raise ValueError("All maps in a package must have matching square dimensions")
            source_hash = sha256(package) if package.is_file() else None
            scratch = Path(td) / "package"
            shutil.copytree(root, scratch)
            base_size = None
            for name in ("master", "color"):
                p = scratch / f"{name}.png"
                if p.exists():
                    size, _ = _image_info(p)
                    if base_size is None:
                        base_size = size
                    elif size != base_size:
                        raise ValueError("Existing master and color maps have different dimensions")
            for key, src in imports:
                if not src.is_file():
                    raise FileNotFoundError(src)
                size, _ = _image_info(src)
                if base_size and size != base_size:
                    raise ValueError(f"{key} is {size[0]}px, expected package size {base_size[0]}px")
                if key in GRAY_MAPS and not _is_grayscale(src):
                    raise ValueError(f"{key} must be grayscale; chromatic paint is never silently desaturated")
                shutil.copy2(src, scratch / f"{key}.png")
            maps = sorted(p.name for p in scratch.glob("*.png"))
            if "master.png" not in maps:
                raise ValueError("Package must contain master.png")
            if "color.png" not in maps:
                raise ValueError("Package must contain color.png as its linked paint/albedo baseline")
            existing = []
            if output.exists():
                existing = [int(m.group(1)) for p in output.glob(f"{pid}_rev*.json")
                            if (m := re.fullmatch(re.escape(pid) + r"_rev(\d+)\.json", p.name))]
                existing += [int(m.group(1)) for p in output.glob(f"{pid}_rev*")
                             if (m := re.fullmatch(re.escape(pid) + r"_rev(\d+)", p.name))]
            revision = max(existing, default=0) + 1
            dest = output / f"{pid}_rev{revision:03d}"
            if dest.exists():
                raise FileExistsError(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(scratch, dest)
            manifest = {
                "package_id": pid, "revision": revision,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "source_package": str(package), "source_package_sha256": source_hash,
                "source_maps": {k: {"path": str(src), "sha256": sha256(src)} for k, src in imports},
                "imported_maps": keys, "maps": maps,
                "catalog": catalog_row,
                "notes": "Original package retained; selected mappings only were replaced.",
            }
            (dest / "return.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            return dest
        finally:
            if temp is not None:
                temp.cleanup()


def build_blender_material(package, material_name=None, scale_m=None,
                           object=None, slot_index=None, replace_slot=False,
                           catalog_path=None, palettes_path=None, palette_option=None):
    """Build a new metric-repeat Blender PBR material from a package folder/ZIP.

    `object` and `slot_index` are optional. An occupied slot is preserved unless
    replace_slot=True; existing Blender materials are never edited in place.
    """
    import bpy
    pkg = Path(package).expanduser().resolve()
    temp = tempfile.TemporaryDirectory(prefix="caelmor-blender-package-", dir=Path(__file__).resolve().parent) if pkg.is_file() else None
    root = _package_root(pkg, temp)
    try:
        returned = json.loads((root / "return.json").read_text(encoding="utf-8")) if (root / "return.json").exists() else {}
        metadata_path = root / "metadata.json"
        meta = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        pid = returned.get("package_id", meta.get("id", root.name))
        catalog = {}
        if catalog_path:
            rows = _catalog_rows(json.loads(Path(catalog_path).read_text(encoding="utf-8")))
            catalog = next((r for r in rows if r.get("id") == pid), {})
        if object is not None:
            if slot_index is None or slot_index < 0:
                raise ValueError("A nonnegative slot_index is required when assigning to an object")
            if slot_index < len(object.material_slots) and object.material_slots[slot_index].material and not replace_slot:
                raise ValueError("Target slot already has a material; pass replace_slot=True to replace it")
        mat = bpy.data.materials.new(material_name or f"Caelmor | {pid} | rev {returned.get('revision', 0):03d}")
        mat.use_nodes = True
        mat["caelm_material_package"] = pid
        mat["caelm_package_revision"] = int(returned.get("revision", meta.get("revision", 0)))
        mat["caelm_user_override"] = True
        mat.use_fake_user = True
        nodes, links = mat.node_tree.nodes, mat.node_tree.links
        shader = nodes.get("Principled BSDF")
        if shader is None: shader = nodes.new("ShaderNodeBsdfPrincipled")
        shader.location = (500, 80)
        uv = nodes.new("ShaderNodeUVMap"); uv.uv_map = "UV0_Metric"; uv.label = "Architectural generator UV0_Metric"; uv.location = (-800, 0)
        mapping = nodes.new("ShaderNodeMapping"); mapping.label = "Tile size in metres"; mapping.location = (-600, 0)
        tile = scale_m if scale_m is not None else catalog.get("scale_m", meta.get("scale_m", 1.0))
        if isinstance(tile, (list, tuple)):
            if len(tile) != 2 or any(float(v) <= 0 for v in tile):
                raise ValueError("scale_m arrays must contain two positive metre dimensions")
            mapping.inputs["Scale"].default_value = (1.0 / float(tile[0]), 1.0 / float(tile[1]), 1.0)
        else:
            tile = float(tile)
            if tile <= 0: raise ValueError("scale_m must be greater than zero")
            mapping.inputs["Scale"].default_value = (1.0 / tile, 1.0 / tile, 1.0)
        links.new(uv.outputs["UV"], mapping.inputs["Vector"])
        color_path = root / "color.png"
        color_img = bpy.data.images.load(str(color_path), check_existing=True)
        color_img.colorspace_settings.name = "sRGB"
        if not color_img.packed_file:
            color_img.pack()
        tex = nodes.new("ShaderNodeTexImage"); tex.image = color_img; tex.extension = "REPEAT"; tex.label = "Color / grayscale paint baseline"; tex.location = (-350, 220)
        links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
        # Palette contract: family -> option -> four #RRGGBB stops; grayscale drives a color ramp.
        color_out = tex.outputs["Color"]
        palette_file = Path(palettes_path) if palettes_path else (Path(catalog_path).parent / "palettes.json" if catalog_path else None)
        palette_data = json.loads(palette_file.read_text(encoding="utf-8")) if palette_file and palette_file.exists() else {}
        family = catalog.get("palette", catalog.get("family", meta.get("palette", meta.get("family"))))
        options = palette_data.get(family, {}) if family else {}
        option = palette_option or catalog.get("palette_option") or meta.get("palette_option")
        if option and option not in options:
            raise ValueError(f"Palette option {option!r} is not defined for family {family!r}")
        rgb_pixels = color_img.pixels[:]
        is_grayscale = all(abs(rgb_pixels[i] - rgb_pixels[i + 1]) < 1e-5 and
                           abs(rgb_pixels[i + 1] - rgb_pixels[i + 2]) < 1e-5
                           for i in range(0, len(rgb_pixels), 4))
        if option and is_grayscale:
            stops = options[option]
            if len(stops) != 4:
                raise ValueError(f"Palette {family}/{option} must have exactly four hex stops")
            ramp = nodes.new("ShaderNodeValToRGB"); ramp.label = f"{family} palette: {option}"; ramp.location = (0, 220)
            ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
            for index, value in enumerate(stops):
                if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value): raise ValueError(f"Invalid palette color: {value}")
                rgba = tuple(_srgb_linear(value[i:i+2]) for i in (1, 3, 5)) + (1.0,)
                el = ramp.color_ramp.elements[0] if index == 0 else ramp.color_ramp.elements.new(index / 3)
                el.position = index / 3; el.color = rgba
            ramp.color_ramp.interpolation = "LINEAR"
            links.new(tex.outputs["Color"], ramp.inputs["Fac"])
            color_out = ramp.outputs["Color"]
        overlay_path = root / "overlay.png"
        if overlay_path.exists():
            oi = bpy.data.images.load(str(overlay_path), check_existing=True); oi.colorspace_settings.name = "sRGB"
            if not oi.packed_file:
                oi.pack()
            ot = nodes.new("ShaderNodeTexImage"); ot.image = oi; ot.extension = "REPEAT"; ot.label = "Optional authored overlay"; ot.location = (-350, -220)
            links.new(mapping.outputs["Vector"], ot.inputs["Vector"])
            over = nodes.new("ShaderNodeMixRGB"); over.blend_type = "MIX"; over.label = "Overlay alpha"; over.location = (240, 220)
            links.new(color_out, over.inputs["Color1"]); links.new(ot.outputs["Color"], over.inputs["Color2"]); links.new(ot.outputs["Alpha"], over.inputs["Fac"])
            color_out = over.outputs["Color"]
        links.new(color_out, shader.inputs["Base Color"])
        for key, input_name in (("roughness", "Roughness"), ("metallic", "Metallic")):
            p = root / f"{key}.png"
            if p.exists():
                im = bpy.data.images.load(str(p), check_existing=True); im.colorspace_settings.name = "Non-Color"
                if not im.packed_file:
                    im.pack()
                n = nodes.new("ShaderNodeTexImage"); n.image = im; n.extension = "REPEAT"; n.label = key.title(); n.location = (-350, -450 if key == "roughness" else -650)
                links.new(mapping.outputs["Vector"], n.inputs["Vector"]); links.new(n.outputs["Color"], shader.inputs[input_name])
        p = root / "normal.png"
        if p.exists():
            im = bpy.data.images.load(str(p), check_existing=True); im.colorspace_settings.name = "Non-Color"
            if not im.packed_file:
                im.pack()
            n = nodes.new("ShaderNodeTexImage"); n.image = im; n.extension = "REPEAT"; n.label = "Tangent normal"; n.location = (-350, -850)
            nm = nodes.new("ShaderNodeNormalMap"); nm.space = "TANGENT"; nm.uv_map = uv.uv_map
            nm.location = (240, -350)
            links.new(mapping.outputs["Vector"], n.inputs["Vector"]); links.new(n.outputs["Color"], nm.inputs["Color"]); links.new(nm.outputs["Normal"], shader.inputs["Normal"])
        output = next((n for n in nodes if n.type == "OUTPUT_MATERIAL"), None)
        if output: links.new(shader.outputs["BSDF"], output.inputs["Surface"])
        if object is not None:
            while len(object.material_slots) <= slot_index:
                object.data.materials.append(None)
            object.material_slots[slot_index].material = mat
        return mat
    finally:
        if temp is not None: temp.cleanup()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", required=True, type=Path, help="Authoritative package folder or ZIP")
    ap.add_argument("--output", required=True, type=Path, help="Parent folder for new revisioned outputs")
    ap.add_argument("--package-id")
    ap.add_argument("--catalog", type=Path, help="Optional catalog.json for identity validation and scale metadata")
    ap.add_argument("--import-map", action="append", default=[], type=parse_mapping, metavar="MAP=PNG",
                    help="Explicit map replacement; repeat for multiple selected mappings")
    args = ap.parse_args(argv)
    dest = return_paint(args.package, args.import_map, args.output, args.package_id, args.catalog)
    print(dest)
    return 0


def blender_main(argv=None):
    ap = argparse.ArgumentParser(description="Create a repeatable Blender PBR material from a Caelmor package")
    ap.add_argument("--blender-package", required=True, type=Path)
    ap.add_argument("--name")
    ap.add_argument("--scale-m", type=float)
    ap.add_argument("--catalog", type=Path)
    ap.add_argument("--palettes", type=Path)
    ap.add_argument("--palette-option", choices=("native", "weathered", "deep"))
    ap.add_argument("--save-blend", type=Path, help="Optional output .blend path")
    args = ap.parse_args(argv)
    output=args.save_blend.expanduser().resolve() if args.save_blend else None
    if output and output.exists():
        ap.error(f"Choose a fresh Blender filename: {output}")
    material = build_blender_material(args.blender_package, args.name, args.scale_m,
                                      catalog_path=args.catalog, palettes_path=args.palettes,
                                      palette_option=args.palette_option)
    if output:
        import bpy
        output.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print(material.name)
    return 0


if __name__ == "__main__":
    if "bpy" in sys.modules:
        blender_args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
        if "--blender-package" in blender_args:
            raise SystemExit(blender_main(blender_args))
    else:
        raise SystemExit(main())
