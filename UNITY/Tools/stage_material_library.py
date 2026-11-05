"""Stage explicitly selected original Caelmor painting baselines for Unity.

Requires Pillow. Source packages and master textures are read only. The output
descriptor is tooling provenance, not a new production content contract.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile

from PIL import Image, ImageChops


REPOSITORY = Path(__file__).resolve().parents[2]
LIBRARY = REPOSITORY / "MEDIA/Materials"
DEFAULT_OUTPUT = REPOSITORY / "UNITY/Assets/_Project/World/Architecture/Materials"
COPY_CHANNELS = ("color", "normal", "roughness", "metallic")


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def png(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG", optimize=False, compress_level=6)
    return output.getvalue()


def pack_metallic_smoothness(metallic: bytes, roughness: bytes) -> bytes:
    """Standard shader: metallic in R, linear smoothness=1-roughness in A."""
    with Image.open(BytesIO(metallic)) as source:
        metal = source.convert("L")
    with Image.open(BytesIO(roughness)) as source:
        rough = source.convert("L")
    if metal.size != rough.size:
        raise ValueError("Metallic and roughness resolutions differ")
    zero = Image.new("L", metal.size, 0)
    smooth = rough.point(lambda value: 255 - value)
    return png(Image.merge("RGBA", (metal, zero, zero, smooth)))


def prepare(identity: str, library: Path = LIBRARY) -> dict[str, bytes]:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", identity):
        raise ValueError(f"Invalid stable material ID: {identity!r}")
    catalog = json.loads((library / "catalog.json").read_text(encoding="utf-8"))
    record = next((r for r in catalog["materials"] if r["id"] == identity), None)
    if record is None:
        raise ValueError(f"Unknown catalog material ID: {identity}")
    package_path = library / "packages" / f"{identity}.zip"
    package_bytes = package_path.read_bytes()
    files = {}
    with ZipFile(BytesIO(package_bytes)) as archive:
        metadata_bytes = archive.read(f"{identity}/metadata.json")
        metadata = json.loads(metadata_bytes)
        if metadata["id"] != identity or metadata["scale_m"] != record["scale_m"]:
            raise ValueError(f"Catalog/package identity or physical repeat conflict: {identity}")
        if metadata.get("normal_space") != "tangent +Y":
            raise ValueError(f"Unsupported source normal convention: {identity}")
        for channel in COPY_CHANNELS:
            files[f"{channel}.png"] = archive.read(f"{identity}/{channel}.png")
        master = archive.read(f"{identity}/master.png")
    if (library / "masters" / f"{identity}.png").read_bytes() != master:
        raise ValueError(f"Packaged master differs from authoritative master: {identity}")
    with Image.open(BytesIO(files["color.png"])) as source:
        rgb = source.convert("RGB")
        red, green, blue = rgb.split()
        if ImageChops.difference(red, green).getbbox() or ImageChops.difference(green, blue).getbbox():
            raise ValueError(f"Source is no longer an unpainted grayscale baseline: {identity}")
        resolution = list(rgb.size)
    files["metallic_smoothness.png"] = pack_metallic_smoothness(files["metallic.png"], files["roughness.png"])
    scale = record["scale_m"]
    if len(scale) != 2 or any(float(v) <= 0 for v in scale):
        raise ValueError(f"Invalid physical repeat: {identity}")
    descriptor = {
        "id": identity,
        "scale_m": scale,
        "resolution": resolution,
        "source_package": f"MEDIA/Materials/packages/{identity}.zip",
        "source_package_sha256": digest(package_bytes),
        "source_metadata_sha256": digest(metadata_bytes),
        "source_master_sha256": digest(master),
        "rights": "Original Caelmor procedural grayscale baseline and PBR companions; see MEDIA/Materials/PRODUCTION_REPORT.md.",
        "usage": "Explicit artist binding only; requires source metric UV0. No generator-to-library mapping is inferred.",
        "color_space": "color.png: sRGB; normal and scalar/packed maps: linear",
        "normal_space": "tangent +Y",
        "packing": "metallic_smoothness.png R=metallic, G=B=0, A=1-roughness; linear UNorm8",
        "generated_files_sha256": {name: digest(data) for name, data in sorted(files.items())},
    }
    files["material.json"] = (json.dumps(descriptor, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return files


def validate_destination(destination: Path, files: dict[str, bytes]) -> None:
    """Preflight the whole selection before any file writes."""
    descriptor_path = destination / "material.json"
    old_hashes = {}
    if descriptor_path.exists():
        previous = json.loads(descriptor_path.read_text(encoding="utf-8"))
        if previous.get("id") != destination.name:
            raise ValueError(f"Destination identity conflict: {destination}")
        old_hashes = previous.get("generated_files_sha256", {})
        # Preserve hand changes to provenance too; resource refresh should be
        # performed explicitly from a clean generated baseline.
        expected_fields = {"id", "scale_m", "resolution", "source_package", "source_package_sha256",
                           "source_metadata_sha256", "source_master_sha256", "rights", "usage",
                           "color_space", "normal_space", "packing", "generated_files_sha256"}
        if set(previous) != expected_fields:
            raise ValueError(f"Edited or unsupported material descriptor: {descriptor_path}")
        current = json.loads(files["material.json"])
        if (previous.get("source_package_sha256") == current["source_package_sha256"]
                and previous != current):
            raise ValueError(f"Edited material descriptor; preserved {descriptor_path}")
    for name, data in files.items():
        path = destination / name
        if not path.exists() or path.read_bytes() == data:
            continue
        if name == "material.json":
            # A changed descriptor must still describe all currently staged
            # resource bytes, and never conceal edits to those files.
            continue
        if digest(path.read_bytes()) != old_hashes.get(name):
            raise ValueError(f"Artist-edited generated texture conflict; preserved {path}")


def retain_equivalent_packed_png(destination: Path, files: dict[str, bytes]) -> None:
    """Pillow/zlib versions may encode identical pixels to different PNG bytes.

    Preserve a previously generated packed map when its bytes still match the
    recorded hash and every decoded channel matches this run. This cannot
    accept artist pixel edits or changes to copied source channels.
    """
    descriptor_path = destination / "material.json"
    packed_path = destination / "metallic_smoothness.png"
    if not descriptor_path.exists() or not packed_path.exists():
        return
    previous = json.loads(descriptor_path.read_text(encoding="utf-8"))
    current = json.loads(files["material.json"])
    if previous.get("source_package_sha256") != current["source_package_sha256"]:
        return
    old_bytes = packed_path.read_bytes()
    if digest(old_bytes) != previous.get("generated_files_sha256", {}).get(packed_path.name):
        return
    with Image.open(BytesIO(old_bytes)) as old, Image.open(BytesIO(files[packed_path.name])) as new:
        if old.mode != new.mode or old.size != new.size or old.tobytes() != new.tobytes():
            return
    files[packed_path.name] = old_bytes
    current["generated_files_sha256"][packed_path.name] = digest(old_bytes)
    files["material.json"] = (descriptor_path.read_bytes() if previous == current else
                              (json.dumps(current, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def stage(identities: list[str], output: Path = DEFAULT_OUTPUT) -> list[dict]:
    output = output.resolve()
    if not output.is_relative_to(REPOSITORY):
        raise ValueError("Staged assets must stay inside the designated repository checkout")
    selected = [(identity, prepare(identity)) for identity in dict.fromkeys(identities)]
    for identity, files in selected:
        retain_equivalent_packed_png(output / identity, files)
        validate_destination(output / identity, files)
    results = []
    for identity, files in selected:
        destination = output / identity
        destination.mkdir(parents=True, exist_ok=True)
        changed = 0
        for name, data in files.items():
            path = destination / name
            if not path.exists() or path.read_bytes() != data:
                path.write_bytes(data)
                changed += 1
        results.append({"id": identity, "files": len(files), "changed": changed,
                        "bytes": sum(len(data) for data in files.values())})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", action="append", required=True, help="Existing stable catalog ID; repeat to select more")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(stage(args.id, args.output), indent=2))


if __name__ == "__main__":
    main()
