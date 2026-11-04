"""Targeted regressions for the opt-in crafted construction curves."""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.engine import generate, geometry_hash, validate
from caelmor_architecture.model import Settings
from caelmor_architecture.roof import roof_courses, roof_faces, roof_join_kind, roof_topology
from test_world import _ray_hits


def _edges(poly):
    return {tuple(sorted((a, b))) for a, b in zip(poly, poly[1:] + poly[:1])}


def _buffer_for(buffers, suffix):
    matches = [buffer for buffer in buffers if buffer.name.endswith(suffix)]
    if len(matches) != 1:
        raise AssertionError(f"Expected one buffer ending in {suffix!r}, got {len(matches)}")
    return matches[0]


class ConstructionCurveTests(unittest.TestCase):
    def _generate(self, region, function, seed, mode="SOLID", crafted=True):
        settings = Settings(seed=seed, function=function, region=region,
                            detail="LOW", geometry_mode=mode, use_grammar=True,
                            world_aware=True, crafted_curves=crafted)
        plan, buffers = generate(settings)
        report = validate(plan, buffers)
        self.assertTrue(report["valid"], report["errors"][:8])
        return plan, buffers

    def test_lowmark_smithy_swept_gable_drains_meets_at_seams_and_clears_bents(self):
        for seed, mode in ((7, "SOLID"), (19, "EFFICIENT")):
            with self.subTest(seed=seed, mode=mode):
                plan, buffers = self._generate("LOWMARK", "SMITHY", seed, mode)
                mass = next(zone for zone in plan.world_zones if zone.key == "forge_hall")
                patches = mass.plan.custom_roof_sources
                self.assertGreater(len(patches), 2)
                self.assertTrue(all(patch.swept for patch in patches))
                resolved = roof_faces(mass.plan)
                points, _, edges = roof_topology(resolved)
                joins = [roof_join_kind(points, resolved, users) for users in edges.values()
                         if len(users) == 2]
                self.assertEqual(joins.count("ridge"), 1)
                self.assertTrue(set(joins) <= {"profile", "ridge"})

                # Construction seams lie behind course butts on both slopes.
                x0, _, x1, _ = mass.bounds
                o = mass.plan.settings.overhang
                ridge = (x0+x1)*.5
                for direction, eave in ((1,x0-o),(-1,x1+o)):
                    limit = abs(eave-ridge)
                    allowed = [t for _, t, _ in roof_courses(mass.plan, 0, direction, limit)]
                    cuts = {x for patch in patches for x, _ in patch.poly
                            if 1e-7 < direction*(x-eave) < limit-1e-7}
                    self.assertTrue(all(any(abs(direction*(x-eave)-t)<1e-7 for t in allowed)
                                        for x in cuts))

                # Each strip shares its complete boundary with its neighbor at
                # the same height, so the swept cover has no geometric seam gap.
                shared_edges = 0
                for i, first in enumerate(patches):
                    for second in patches[i + 1:]:
                        common = _edges(first.poly) & _edges(second.poly)
                        for edge in common:
                            shared_edges += 1
                            for x, y in edge:
                                self.assertAlmostEqual(first.height(x, y),
                                                       second.height(x, y), places=7)
                self.assertEqual(shared_edges, len(patches) - 1)

                x0, y0, x1, y1 = mass.bounds
                ridge_x = (x0 + x1) * .5
                for y in (y0 + .1, (y0 + y1) * .5, y1 - .1):
                    self.assertGreater(mass.roof_height(x0 + .2, y),
                                       mass.roof_height(x0, y))
                    self.assertGreater(mass.roof_height(ridge_x, y),
                                       mass.roof_height(x0 + .2, y))
                    self.assertGreater(mass.roof_height(x1 - .2, y),
                                       mass.roof_height(x1, y))
                    self.assertGreater(mass.roof_height(ridge_x, y),
                                       mass.roof_height(x1 - .2, y))

                bent_buffers = [b for b in buffers if b.world_zone == "forge_hall"
                                and (b.name.endswith("smithy.primary_end_bent")
                                     or b.name.endswith("smithy.tie_knees.front")
                                     or b.name.endswith("smithy.tie_knees.rear"))]
                self.assertEqual(len(bent_buffers), 3)
                for bent in bent_buffers:
                    for x, y, z in bent.vertices:
                        roof_z = mass.roof_height(x, y)
                        if math.isfinite(roof_z):
                            self.assertLessEqual(z, roof_z - .12 + .002,
                                                 (bent.name, (x, y, z), roof_z))

    def test_thornfell_passage_air_is_open_above_old_crown_and_arch_still_blocks_above_new(self):
        for seed, mode in ((7, "SOLID"), (19, "EFFICIENT")):
            with self.subTest(seed=seed, mode=mode):
                plan, buffers = self._generate("THORNFELL", "GATEHOUSE", seed, mode)
                portal = next(zone for zone in plan.world_zones
                              if zone.key == "gatehouse_portal")
                arch = portal.plan.passage_arch
                self.assertAlmostEqual(arch["rise"], .82)
                self.assertEqual(len(arch["stations"]), 17)
                cx = portal.bounds[0] + portal.width * .5
                # At this elevation the legacy .60m arch is closed while the
                # crafted .82m crown leaves a real ray through the portal.
                origin = (cx, -1., portal.base + arch["spring"] + .65)
                air_hits = _ray_hits(origin, (0., 1., 0.), 2.5, buffers)
                self.assertFalse(air_hits, "new arch crown does not leave the promised air ray")

                above_crown = (cx, -1., portal.base + arch["spring"] + arch["rise"] + .10)
                blocked = _ray_hits(above_crown, (0., 1., 0.), 2.5, buffers)
                self.assertTrue(blocked, "ray above the new crown should meet the wall/arch")

    def test_mire_ribs_follow_every_bow_station_only_when_enabled(self):
        for seed, mode in ((7, "SOLID"), (19, "EFFICIENT")):
            with self.subTest(seed=seed, mode=mode):
                plan, buffers = self._generate("MIRE", "MILLER", seed, mode)
                mass = next(zone for zone in plan.world_zones if zone.key == "mire_longhouse")
                ribs = _buffer_for(buffers, "mire_bow_roof_ribs")
                self.assertEqual(len(ribs.vertices) % 8, 0)
                sections = len(ribs.vertices) // 8
                self.assertEqual(sections % 3, 0)  # LOW detail generates three ribs.
                stations_per_rib = sections // 3
                self.assertGreaterEqual(stations_per_rib, 5)
                for rib_index in range(3):
                    centers = []
                    for station_index in range(stations_per_rib):
                        ring = ribs.vertices[(rib_index * stations_per_rib + station_index) * 8:
                                             (rib_index * stations_per_rib + station_index + 1) * 8]
                        center = tuple(sum(point[axis] for point in ring) / 8
                                       for axis in range(3))
                        centers.append(center)
                    self.assertEqual(len({round(point[1], 7) for point in centers}),
                                     stations_per_rib)
                    for x, y, z in centers:
                        self.assertAlmostEqual(z, mass.roof_height(x, y) - .28, places=6)

                _, legacy_buffers = self._generate(
                    "MIRE", "MILLER", seed, mode, crafted=False)
                legacy_ribs = _buffer_for(legacy_buffers, "mire_bow_roof_ribs")
                # Straight segment beams duplicate their ends; the crafted
                # sweep has one eight-vertex section per roof station.
                self.assertNotEqual(len(legacy_ribs.vertices), len(ribs.vertices))
                self.assertNotEqual(geometry_hash(buffers), geometry_hash(legacy_buffers))

    def test_option_defaults_off_and_emberholt_geometry_is_unchanged(self):
        self.assertFalse(Settings().crafted_curves)
        self.assertEqual(Settings(), Settings(crafted_curves=False))
        for seed, mode in ((7, "SOLID"), (19, "EFFICIENT")):
            with self.subTest(seed=seed, mode=mode):
                _, ordinary = self._generate("EMBERHOLT", "SMITHY", seed, mode,
                                             crafted=False)
                _, opted_in = self._generate("EMBERHOLT", "SMITHY", seed, mode,
                                             crafted=True)
                self.assertEqual(geometry_hash(ordinary), geometry_hash(opted_in))


if __name__ == "__main__":
    unittest.main(verbosity=2)
