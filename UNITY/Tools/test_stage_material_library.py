"""Channel fidelity, idempotence, and edit-protection checks for library staging."""
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

import stage_material_library as stage


class MaterialStagingTests(unittest.TestCase):
    def test_standard_packing_retains_linear_values(self):
        metal = Image.new("L", (3, 1))
        rough = Image.new("L", (3, 1))
        metal.putdata([0, 113, 255])
        rough.putdata([0, 127, 255])
        packed = stage.pack_metallic_smoothness(stage.png(metal), stage.png(rough))
        with Image.open(BytesIO(packed)) as result:
            self.assertEqual([result.getpixel((x, 0)) for x in range(3)], [(0, 0, 0, 255), (113, 0, 0, 128), (255, 0, 0, 0)])

    def test_real_baselines_repeat_and_protect_edits(self):
        identities = ["split_oak_shingle", "forged_iron"]
        before = {(stage.LIBRARY / "masters" / f"{identity}.png"): (stage.LIBRARY / "masters" / f"{identity}.png").read_bytes()
                  for identity in identities}
        # Disposable tests remain within the designated checkout.
        with tempfile.TemporaryDirectory(prefix="material-check-", dir=Path(__file__).resolve().parent) as temp:
            output = Path(temp)
            first = stage.stage(identities, output)
            self.assertTrue(all(record["changed"] == 6 for record in first))
            second = stage.stage(identities, output)
            self.assertTrue(all(record["changed"] == 0 for record in second))
            # Simulate an older Pillow/zlib writer's valid byte-distinct PNG.
            packed_path = output / "forged_iron/metallic_smoothness.png"
            with Image.open(packed_path) as packed:
                encoded = BytesIO()
                packed.save(encoded, format="PNG", compress_level=0)
            packed_path.write_bytes(encoded.getvalue())
            descriptor_path = output / "forged_iron/material.json"
            descriptor = json.loads(descriptor_path.read_text())
            descriptor["generated_files_sha256"][packed_path.name] = stage.digest(encoded.getvalue())
            descriptor_path.write_text(json.dumps(descriptor, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            third = stage.stage(identities, output)
            self.assertTrue(all(record["changed"] == 0 for record in third))
            self.assertEqual(packed_path.read_bytes(), encoded.getvalue())
            color = output / "forged_iron/color.png"
            color.write_bytes(b"artist edit")
            original_first = (output / "split_oak_shingle/color.png").read_bytes()
            with self.assertRaisesRegex(ValueError, "Artist-edited"):
                stage.stage(identities, output)
            self.assertEqual(color.read_bytes(), b"artist edit")
            self.assertEqual((output / "split_oak_shingle/color.png").read_bytes(), original_first)
            color.write_bytes(stage.prepare("forged_iron")["color.png"])
            descriptor_path = output / "forged_iron/material.json"
            descriptor = json.loads(descriptor_path.read_text())
            descriptor["scale_m"] = [100, 100]
            descriptor_path.write_text(json.dumps(descriptor))
            with self.assertRaisesRegex(ValueError, "Edited material descriptor"):
                stage.stage(identities, output)
            self.assertEqual(json.loads(descriptor_path.read_text())["scale_m"], [100, 100])
        for path, original in before.items():
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
