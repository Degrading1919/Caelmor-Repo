"""Independent regression checks for the expanded Caelmor exterior grammar.

Run with ``python -m unittest discover -s tests -p test_expansion.py -v``.
These checks cover authored generator geometry only; they are not a structural
engineering or target-engine certification.
"""

import unittest

from caelmor_architecture.engine import compare_geometry_modes, generate, validate
from caelmor_architecture.facade import frame_layout
from caelmor_architecture.materials import surface_tint
from caelmor_architecture.model import Settings, make_plan, resolve_settings, style_for
from caelmor_architecture.profiles import CONTEXTS, REGIONS, TYPE_SPECS


class ExpandedGrammarTests(unittest.TestCase):
    def test_every_local_context_resolves_for_every_supported_type_and_wealth(self):
        """Cross all public profile axes without building 1,200 roof meshes."""
        self.assertEqual(set(REGIONS), {"LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT"})
        self.assertEqual(len(TYPE_SPECS), 20)
        rows = 0
        for region, contexts in CONTEXTS.items():
            for context in contexts:
                for function in TYPE_SPECS:
                    for wealth in ("MODEST", "ESTABLISHED", "AFFLUENT"):
                        with self.subTest(region=region, context=context,
                                          function=function, wealth=wealth):
                            requested = Settings(region=region, context=context,
                                                  function=function, wealth=wealth,
                                                  use_grammar=True)
                            effective = resolve_settings(requested)
                            self.assertEqual(effective.region, region)
                            self.assertEqual(effective.context, context)
                            self.assertEqual(effective.function, function)
                            self.assertEqual(effective.wealth, wealth)
                            effective.check()
                            rows += 1
        self.assertGreaterEqual(rows, 1000)

    def test_all_twenty_types_have_valid_nonidentical_semantic_geometry(self):
        """Type IDs must produce actual geometry, not just renamed settings."""
        signatures = {}
        for function in TYPE_SPECS:
            with self.subTest(function=function):
                requested = Settings(function=function, use_grammar=True,
                                     region="LOWMARK", wealth="ESTABLISHED", seed=41)
                plan, buffers = generate(requested)
                report = validate(plan, buffers)
                self.assertTrue(report["valid"], report["errors"])
                self.assertEqual(plan.type_spec, TYPE_SPECS[function])
                self.assertTrue(plan.type_spec.features)
                scheduled_openings = [opening for row in plan.facade_records
                                      for opening in row["openings"]]
                if function == "GATEHOUSE":
                    self.assertTrue(any(o.get("role") == "passage_exit"
                                        for o in scheduled_openings))
                else:
                    self.assertTrue(any(o["kind"] == "door" for o in scheduled_openings),
                                    f"{function} has no scheduled exterior entry")
                if function == "STABLE":
                    stall_doors = [o for o in scheduled_openings
                                   if o["kind"] == "door" and str(o.get("role", "")).startswith("stall_")]
                    self.assertGreaterEqual(len(stall_doors), 2, scheduled_openings)
                # Feature-sensitive mesh names/materials plus resolved massing make
                # this sensitive to a type that only changes its display label.
                signatures[function] = (
                    plan.settings.footprint, plan.settings.floors,
                    tuple(sorted((b.name, b.material, b.layer,
                                  len(b.vertices), len(b.faces)) for b in buffers)),
                )
        self.assertGreaterEqual(len(set(signatures.values())), 16)

    def test_wealth_changes_mass_and_surface_while_upkeep_changes_wear_only(self):
        base = dict(function="COTTAGE", use_grammar=True, region="LOWMARK",
                    context="RURAL", craftsmanship="STANDARD", age=100)
        modest = Settings(**base, wealth="MODEST", maintenance=.7)
        affluent = Settings(**base, wealth="AFFLUENT", maintenance=.7)
        modest_plan, modest_buffers = generate(modest)
        affluent_plan, affluent_buffers = generate(affluent)
        self.assertNotEqual((modest_plan.settings.width, modest_plan.settings.depth,
                             modest_plan.settings.pitch),
                            (affluent_plan.settings.width, affluent_plan.settings.depth,
                             affluent_plan.settings.pitch))
        self.assertNotEqual(style_for(modest_plan.settings).roof_cover,
                            style_for(affluent_plan.settings).roof_cover)
        affluent_lowmark=style_for(affluent_plan.settings)
        self.assertEqual(affluent_lowmark.construction,"ASHLAR")
        self.assertEqual(affluent_lowmark.wall_material,"stone")
        rich_mire=style_for(Settings(function="COTTAGE",region="MIRE",wealth="AFFLUENT"))
        self.assertEqual(rich_mire.foundation_mode,"PIERS")
        self.assertEqual(rich_mire.roof_cover,"SHINGLE")
        self.assertNotEqual([(b.name, b.vertices, b.faces) for b in modest_buffers],
                            [(b.name, b.vertices, b.faces) for b in affluent_buffers])

        maintained = Settings(**base, wealth="ESTABLISHED", maintenance=1.0)
        neglected = Settings(**base, wealth="ESTABLISHED", maintenance=0.0)
        maintained_plan, maintained_buffers = generate(maintained)
        neglected_plan, neglected_buffers = generate(neglected)
        self.assertEqual((maintained_plan.settings.width, maintained_plan.settings.depth,
                          maintained_plan.settings.floors, maintained_plan.settings.pitch),
                         (neglected_plan.settings.width, neglected_plan.settings.depth,
                          neglected_plan.settings.floors, neglected_plan.settings.pitch))
        self.assertEqual([(b.name, b.vertices, b.faces) for b in maintained_buffers],
                         [(b.name, b.vertices, b.faces) for b in neglected_buffers])
        self.assertEqual(style_for(maintained_plan.settings).palette,
                         style_for(neglected_plan.settings).palette)
        sample = ((1.0, 0.0, 1.0), (0.0, -1.0, 0.0), "plaster")
        maintained_tint = surface_tint(*sample, maintained_plan, maintained_plan.style,
                                       maintained_plan.settings)
        neglected_tint = surface_tint(*sample, neglected_plan, neglected_plan.style,
                                      neglected_plan.settings)
        self.assertNotEqual(maintained_tint, neglected_tint)

    def test_ancient_age_does_not_generalize_hidden_magic_motifs(self):
        for region in REGIONS:
            ordinary = Settings(region=region, function="COTTAGE", use_grammar=True,
                                age=0, maintenance=.5)
            ancient = Settings(region=region, function="COTTAGE", use_grammar=True,
                               age=250, maintenance=.5)
            plan_a, buffers_a = generate(ordinary)
            plan_b, buffers_b = generate(ancient)
            self.assertEqual(plan_a.type_spec.features, plan_b.type_spec.features)
            self.assertEqual([(b.name, b.layer, b.vertices, b.faces) for b in buffers_a],
                             [(b.name, b.layer, b.vertices, b.faces) for b in buffers_b])

    def test_manual_dimensions_and_legacy_defaults_remain_manual(self):
        manual = Settings(function="COTTAGE", width=13.0, depth=8.0, floors=2,
                          region="THORNFELL", use_grammar=False)
        plan = make_plan(manual)
        self.assertEqual((plan.settings.width, plan.settings.depth, plan.settings.floors),
                         (13.0, 8.0, 2))
        self.assertIs(plan.requested_settings, manual)

    def test_grammar_ignores_overridden_manual_shape_but_validates_active_inputs(self):
        grammar = Settings(
            function="WATCHTOWER", use_grammar=True,
            width=6.0, depth=4.0, wing_width=5.5, wing_depth=13.0,
            floors=0, floor_height=1.0, pitch=10.0, footprint="INVALID_STALE_SHAPE",
        )
        effective = resolve_settings(grammar)
        self.assertEqual(effective.footprint, TYPE_SPECS["WATCHTOWER"].footprint)
        self.assertEqual(effective.floors, TYPE_SPECS["WATCHTOWER"].floors)
        effective.check()

        manual = Settings(**{**grammar.__dict__, "use_grammar": False})
        with self.assertRaises(ValueError):
            resolve_settings(manual)

        for field, invalid_value in (("overhang", 1.0), ("roof_style", "INVALID_ROOF"),
                                     ("region", "INVALID_REGION"),
                                     ("window_density", 2.0)):
            with self.subTest(field=field):
                invalid = Settings(use_grammar=True)
                setattr(invalid, field, invalid_value)
                with self.assertRaises(ValueError):
                    resolve_settings(invalid)

    def test_hip_roof_and_efficient_detail_preserve_closed_core_and_reduce_geometry(self):
        settings = Settings(function="WATCHTOWER", region="THORNFELL",
                            context="PASSWATCH", use_grammar=True,
                            detail="HIGH", seed=23)
        comparison = compare_geometry_modes(settings)
        self.assertEqual(comparison["SOLID"]["roof_style"], "HIP")
        self.assertEqual(comparison["EFFICIENT"]["roof_style"], "HIP")
        for mode in ("SOLID", "EFFICIENT"):
            self.assertTrue(comparison[mode]["valid"], comparison[mode]["errors"])
        self.assertGreater(comparison["vertices_reduction_percent"], 0.0)
        self.assertGreater(comparison["triangles_reduction_percent"], 0.0)

        effective = Settings(**{**settings.__dict__, "geometry_mode":"EFFICIENT"})
        plan, buffers = generate(effective)
        self.assertTrue(validate(plan, buffers)["valid"])
        deck = next(b for b in buffers if b.name == "Continuous roof deck")
        self.assertEqual(deck.topology, "SOLID")
        self.assertTrue(all(b.topology == "SURFACE" for b in buffers
                            if b.layer == "roof" and b.name in (
                                "Split oak shingle courses", "Seasoned shingle cohorts",
                                "Exposed shingle butts", "Replacement shingle cohort",
                                "Concealed roof course bedding")))
        skin = next(b for b in buffers if b.name == "facade_masonry_skin")
        self.assertEqual(skin.topology, "SURFACE")
        core_body = [b for b in buffers if b.name in (
            "facade_walls", "facade_foundation_core", "facade_timber", "Continuous roof deck")]
        self.assertTrue(core_body)
        self.assertTrue(all(b.topology == "SOLID" for b in core_body),
                        [(b.name, b.topology) for b in core_body])

    def test_window_full_assembly_clears_posts_braces_plates_and_gable_members(self):
        """Compare the whole casing/shutter envelope with every scheduled frame member."""
        cases = (
            ("FARMHOUSE", "LOWMARK", "RURAL", "RECT", 1, 60.0),
            ("TOWNHOUSE", "THORNFELL", "STONEWAKE", "RECT", 3, 44.0),
            ("BOATHOUSE", "MIRE", "SORROWMERE", "RECT", 1, 38.0),
            ("INN", "EMBERHOLT", "EMBERFORGES", "L", 2, 42.0),
        )
        for function, region, context, footprint, floors, pitch in cases:
            requested = Settings(function=function, region=region, context=context,
                                 footprint=footprint, floors=floors, pitch=pitch,
                                 width=14.0, depth=10.0, wing_width=4.0,
                                 wing_depth=5.0, window_density=1.5, seed=17)
            plan = make_plan(requested)
            for edge_index, edge in enumerate(plan.edges):
                layout = frame_layout(plan, edge_index, edge)
                for opening in layout["openings"]:
                    if opening["kind"] != "window":
                        continue
                    assembly = opening["assembly_bounds"]
                    for post in layout["principal_posts"]:
                        post_half_width = layout.get("post_half_width", .11)
                        self.assertTrue(post + post_half_width <= assembly["s0"] - .01
                                        or post - post_half_width >= assembly["s1"] + .01,
                                        (function, edge_index, opening, post))
                    for brace in layout["braces"]:
                        pad = brace["width"] * .5 + .01
                        self.assertFalse(_segment_hits_rect(
                            brace["s0"], brace["z0"], brace["s1"], brace["z1"],
                            assembly["s0"]-pad, assembly["z0"]-pad,
                            assembly["s1"]+pad, assembly["z1"]+pad),
                            (function, edge_index, opening, brace))
                    for plate_z in layout["plates"]:
                        self.assertFalse(assembly["z0"] < plate_z < assembly["z1"],
                                         (function, edge_index, opening, plate_z))


def _segment_hits_rect(x0, y0, x1, y1, left, bottom, right, top):
    """Liang-Barsky segment/rectangle intersection, inclusive at contact."""
    dx, dy = x1-x0, y1-y0
    lo, hi = 0.0, 1.0
    for p, q in ((-dx, x0-left), (dx, right-x0),
                 (-dy, y0-bottom), (dy, top-y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        t = q/p
        if p < 0:
            lo = max(lo, t)
        else:
            hi = min(hi, t)
        if lo > hi:
            return False
    return True


if __name__ == "__main__":
    unittest.main(verbosity=2)
