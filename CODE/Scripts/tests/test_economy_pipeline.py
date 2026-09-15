"""Acceptance coverage for the schema-v2 Caelmor economy pipeline.

The suite uses only the Python standard library.  Every build targets a
TemporaryDirectory; it never opens or replaces the repository's canonical DB.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from caelmor_economy_builder import (  # noqa: E402
    ContentError,
    build,
    cross_reference_validate,
    merge_batches,
    semantic_validate_batch,
)
from caelmor_progression_calculator import (  # noqa: E402
    derive_action_math,
    validate_config,
)


SCHEMA_PATH = SCRIPTS_DIR / "caelmor_worker_interchange.schema.json"


def make_item(
    key: str,
    *,
    role: str = "raw_material",
    form: str = "raw",
    regions: list[str] | None = None,
    tags: list[str] | None = None,
    cross_tier_role: str = "limited",
    sources: list[dict] | None = None,
    sinks: list[dict] | None = None,
) -> dict:
    return {
        "slot_id": f"{key}_slot",
        "key": key,
        "display_name": key.replace("_", " ").title(),
        "description": f"Acceptance fixture item: {key}.",
        "category": "core_structures",
        "form": form,
        "economic_role": role,
        "purpose": f"Exercises the analytical contract for {key}.",
        "region_keys": regions or ["lowmark"],
        "tags": tags or [],
        "cross_tier_role": cross_tier_role,
        "rarity_role": "common",
        "external_sources": sources or [],
        "external_sinks": sinks or [],
        "notes": None,
    }


def balance_config() -> dict:
    """Small exact-number config whose expected rates are easy to verify."""
    return {
        "status": "acceptance_fixture",
        "max_level": 30,
        "curve": {
            "kind": "power",
            "total_xp_at_max": 100_000,
            "exponent": 2.0,
        },
        "gather_xp_award_mode": "success",
        "craft_xp_award_mode": "attempt",
        "bands": [
            {
                "id": 1,
                "level_min": 1,
                "level_max": 10,
                "target_xp_per_hour": 3_600,
                "gather_action_seconds": 10.0,
                "craft_action_seconds": 20.0,
                "gather_success_chance": 0.5,
                "weighted_bonus_roll_chance": 0.2,
            },
            {
                "id": 2,
                "level_min": 11,
                "level_max": 20,
                "target_xp_per_hour": 5_400,
                "gather_action_seconds": 10.0,
                "craft_action_seconds": 20.0,
                "gather_success_chance": 0.75,
                "weighted_bonus_roll_chance": 0.2,
            },
            {
                "id": 3,
                "level_min": 21,
                "level_max": 30,
                "target_xp_per_hour": 7_200,
                "gather_action_seconds": 10.0,
                "craft_action_seconds": 20.0,
                "gather_success_chance": 1.0,
                "weighted_bonus_roll_chance": 0.2,
            },
        ],
        "rarity_weights": {
            "common": 3,
            "uncommon": 1,
            "rare": 0.25,
            "special": 0.1,
        },
        "skill_profiles": {},
    }


def valid_batch() -> dict:
    shared_regions = ["lowmark", "thornfell"]
    shared_signature = ["test_mineral"]
    items = [
        make_item(
            "bronze_pick",
            role="tool",
            form="finished",
            sources=[{"relation_type": "starter", "detail": "Starter mining tool."}],
            sinks=[{"relation_type": "equipment_use", "detail": "Equipped as a pick."}],
        ),
        make_item(
            "iron_ore",
            regions=shared_regions,
            tags=shared_signature,
            cross_tier_role="persistent",
        ),
        make_item(
            "coal_lump",
            regions=shared_regions,
            tags=shared_signature,
        ),
        make_item(
            "quartz_fleck",
            regions=shared_regions,
            tags=shared_signature,
        ),
        make_item(
            "iron_bar",
            role="component",
            form="processed",
            sources=[{"relation_type": "salvage", "detail": "Recovered from scrap."}],
            sinks=[{"relation_type": "system_use", "detail": "Repair-system material."}],
        ),
        make_item("iron_hook", role="equipment", form="finished"),
        make_item(
            "orphan_reagent",
            role="component",
            form="refined",
            sinks=[{"relation_type": "system_use", "detail": "Used by a future system."}],
        ),
    ]

    return {
        "batch_id": "acceptance_fixture",
        "notes": "Purpose-built schema-v2 acceptance content.",
        "items": items,
        "gathering_actions": [
            {
                "slot_id": "mine_iron_slot",
                "key": "mine_iron_vein",
                "display_name": "Mine Iron Vein",
                "description": "Mine one shared action through multiple world nodes.",
                "skill_key": "mining",
                "level_band": 1,
                "required_level": 5,
                "purpose": "Tests shared nodes, tools, deterministic rates, and outputs.",
                "region_keys": shared_regions,
                "outputs": [
                    {
                        "item_key": "iron_ore",
                        "quantity": 2,
                        "mode": "guaranteed",
                        "rarity_role": "common",
                        "condition_tag": None,
                        "rng_rationale": None,
                    },
                    {
                        "item_key": "coal_lump",
                        "quantity": 1,
                        "mode": "weighted",
                        "rarity_role": "common",
                        "condition_tag": None,
                        "rng_rationale": "A small mineral bonus pool adds mining texture.",
                    },
                    {
                        "item_key": "quartz_fleck",
                        "quantity": 1,
                        "mode": "weighted",
                        "rarity_role": "uncommon",
                        "condition_tag": None,
                        "rng_rationale": "A small mineral bonus pool adds mining texture.",
                    },
                ],
                "tool_tags": ["pick"],
                "tool_item_keys": ["bronze_pick"],
                "notes": None,
            }
        ],
        "gathering_nodes": [
            {
                "slot_id": "lowmark_vein_slot",
                "key": "lowmark_iron_vein",
                "display_name": "Lowmark Iron Vein",
                "description": "A Lowmark presentation of the shared action.",
                "action_key": "mine_iron_vein",
                "region_key": "lowmark",
                "world_context": "Roadside quarry",
                "interaction_verb": "Mine",
                "depletable": True,
                "respawnable": True,
                "stateful": True,
                "notes": None,
            },
            {
                "slot_id": "thornfell_vein_slot",
                "key": "thornfell_iron_vein",
                "display_name": "Thornfell Iron Vein",
                "description": "A Thornfell presentation of the shared action.",
                "action_key": "mine_iron_vein",
                "region_key": "thornfell",
                "world_context": "Wind-cut ridge",
                "interaction_verb": "Mine",
                "depletable": True,
                "respawnable": True,
                "stateful": True,
                "notes": None,
            },
        ],
        "recipes": [
            {
                "slot_id": "smelt_iron_slot",
                "key": "smelt_iron_bar",
                "display_name": "Smelt Iron Bar",
                "description": "Transforms an early resource in a late band.",
                "skill_key": "smithing",
                "level_band": 3,
                "required_level": 21,
                "purpose": "Tests transformation and long-lived relevance queries.",
                "region_keys": ["lowmark"],
                "inputs": [{"item_key": "iron_ore", "quantity": 3}],
                "outputs": [{"item_key": "iron_bar", "quantity": 1}],
                "station_tag": "furnace",
                "cross_skill_links": ["mining"],
                "notes": None,
            },
            {
                "slot_id": "forge_hook_slot",
                "key": "forge_iron_hook",
                "display_name": "Forge Iron Hook",
                "description": "Consumes the intermediate component.",
                "skill_key": "smithing",
                "level_band": 3,
                "required_level": 25,
                "purpose": "Gives iron bars a modeled recipe sink.",
                "region_keys": ["lowmark"],
                "inputs": [{"item_key": "iron_bar", "quantity": 1}],
                "outputs": [{"item_key": "iron_hook", "quantity": 1}],
                "station_tag": "anvil",
                "cross_skill_links": ["mining"],
                "notes": None,
            },
        ],
    }


class EconomyPipelineAcceptanceTests(unittest.TestCase):
    """End-to-end answerability tests over a temporary analytical database."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tempdir = tempfile.TemporaryDirectory()
        cls.temp_root = Path(cls._tempdir.name)
        cls.input_dir = cls.temp_root / "batches"
        cls.input_dir.mkdir()
        cls.batch = valid_batch()
        (cls.input_dir / "acceptance.json").write_text(
            json.dumps(cls.batch, indent=2), encoding="utf-8"
        )
        cls.config = balance_config()
        cls.config_path = cls.temp_root / "balance.json"
        cls.config_path.write_text(json.dumps(cls.config, indent=2), encoding="utf-8")
        cls.db_path = cls.temp_root / "acceptance.sqlite"
        cls.audit_path = cls.temp_root / "audit.md"
        with contextlib.redirect_stdout(io.StringIO()):
            build(
                cls.input_dir,
                cls.db_path,
                SCHEMA_PATH,
                cls.config_path,
                cls.audit_path,
            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tempdir.cleanup()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextlib.contextmanager
    def database(self):
        """Yield and explicitly close a connection (important on Windows)."""
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()

    def test_schema_v2_and_relational_integrity(self) -> None:
        with self.database() as conn:
            self.assertEqual(
                conn.execute(
                    "SELECT value FROM metadata WHERE key = 'schema_version'"
                ).fetchone()[0],
                "2",
            )
            self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
            nodes = conn.execute(
                "SELECT node_key FROM gathering_nodes "
                "WHERE action_key = 'mine_iron_vein' ORDER BY node_key"
            ).fetchall()
            self.assertEqual(
                [row[0] for row in nodes],
                ["lowmark_iron_vein", "thornfell_iron_vein"],
            )
            outputs = conn.execute(
                "SELECT item_key, mode FROM gathering_action_outputs "
                "WHERE action_key = 'mine_iron_vein' ORDER BY item_key"
            ).fetchall()
            self.assertEqual(len(outputs), 3)
            self.assertEqual({row[1] for row in outputs}, {"guaranteed", "weighted"})

    def test_where_does_item_come_from(self) -> None:
        with self.database() as conn:
            origins = conn.execute(
                "SELECT origin_type, origin_key, action_key, region_key "
                "FROM v_item_origins WHERE item_key = 'iron_ore' ORDER BY origin_key"
            ).fetchall()
        self.assertEqual(len(origins), 2)
        self.assertEqual({row["origin_type"] for row in origins}, {"world_node"})
        self.assertEqual({row["action_key"] for row in origins}, {"mine_iron_vein"})
        self.assertEqual({row["region_key"] for row in origins}, {"lowmark", "thornfell"})

    def test_what_can_item_become(self) -> None:
        with self.database() as conn:
            rows = conn.execute(
                "SELECT recipe_key, output_item_key, required_level "
                "FROM v_item_transformations WHERE input_item_key = 'iron_ore'"
            ).fetchall()
        self.assertEqual(
            [tuple(row) for row in rows],
            [("smelt_iron_bar", "iron_bar", 21)],
        )

    def test_what_skills_and_regions_item_connects(self) -> None:
        with self.database() as conn:
            row = conn.execute(
                "SELECT skills, source_regions, source_count, sink_count "
                "FROM v_item_connections WHERE item_key = 'iron_ore'"
            ).fetchone()
        self.assertEqual(row["skills"], "mining,smithing")
        self.assertEqual(row["source_regions"], "lowmark,thornfell")
        self.assertEqual(row["source_count"], 1)  # actions, not node presentations
        self.assertEqual(row["sink_count"], 1)

    def test_how_long_early_material_stays_relevant(self) -> None:
        with self.database() as conn:
            row = conn.execute(
                "SELECT earliest_source_band, latest_sink_band, progression_band_span, "
                "cross_tier_reuse_count FROM item_metrics WHERE item_key = 'iron_ore'"
            ).fetchone()
        self.assertEqual(tuple(row), (1, 3, 2, 1))

    def test_what_unlocks_at_exact_level(self) -> None:
        with self.database() as conn:
            level_5 = conn.execute(
                "SELECT skill_key, unlock_type, unlock_key FROM v_level_unlocks "
                "WHERE required_level = 5"
            ).fetchall()
            level_21 = conn.execute(
                "SELECT skill_key, unlock_type, unlock_key FROM v_level_unlocks "
                "WHERE required_level = 21"
            ).fetchall()
        self.assertEqual(
            [tuple(row) for row in level_5],
            [("mining", "gathering_action", "mine_iron_vein")],
        )
        self.assertEqual(
            [tuple(row) for row in level_21],
            [("smithing", "recipe", "smelt_iron_bar")],
        )

    def test_which_items_lack_sources_or_sinks(self) -> None:
        with self.database() as conn:
            orphan = conn.execute(
                "SELECT lacks_source, lacks_sink FROM v_item_health "
                "WHERE item_key = 'orphan_reagent'"
            ).fetchone()
            sinkless = {
                row[0]
                for row in conn.execute(
                    "SELECT item_key FROM v_item_health WHERE lacks_sink = 1"
                )
            }
            findings = {
                tuple(row)
                for row in conn.execute(
                    "SELECT finding_type, entity_key FROM validation_findings "
                    "WHERE finding_type IN ('orphan_source', 'dead_end_item')"
                )
            }
        self.assertEqual(tuple(orphan), (1, 0))
        self.assertTrue({"coal_lump", "quartz_fleck"}.issubset(sinkless))
        self.assertIn(("orphan_source", "orphan_reagent"), findings)
        self.assertIn(("dead_end_item", "coal_lump"), findings)

    def test_which_materials_are_potentially_redundant(self) -> None:
        with self.database() as conn:
            keys = {
                row[0]
                for row in conn.execute(
                    "SELECT entity_key FROM validation_findings "
                    "WHERE finding_type = 'potential_redundancy'"
                )
            }
        self.assertEqual(keys, {"iron_ore", "coal_lump", "quartz_fleck"})

    def test_expected_xp_and_yield_per_hour(self) -> None:
        with self.database() as conn:
            action = conn.execute(
                "SELECT target_xp_per_hour, xp_per_action, attempts_per_hour "
                "FROM gathering_actions WHERE action_key = 'mine_iron_vein'"
            ).fetchone()
            rates = {
                row["output_item_key"]: (
                    row["output_probability"], row["expected_quantity_per_hour"]
                )
                for row in conn.execute(
                    "SELECT output_item_key, output_probability, expected_quantity_per_hour "
                    "FROM v_activity_rates WHERE activity_key = 'mine_iron_vein'"
                )
            }
            crafting = conn.execute(
                "SELECT target_xp_per_hour, expected_quantity_per_hour "
                "FROM v_activity_rates WHERE activity_key = 'smelt_iron_bar'"
            ).fetchone()
        self.assertEqual(tuple(action), (3_600.0, 20.0, 360.0))
        self.assertEqual(rates["iron_ore"], (0.5, 360.0))
        self.assertAlmostEqual(rates["coal_lump"][0], 0.075)
        self.assertAlmostEqual(rates["coal_lump"][1], 27.0)
        self.assertAlmostEqual(rates["quartz_fleck"][0], 0.025)
        self.assertAlmostEqual(rates["quartz_fleck"][1], 9.0)
        self.assertEqual(tuple(crafting), (7_200.0, 180.0))

    def test_tools_are_queryable_and_are_modeled_as_sinks(self) -> None:
        with self.database() as conn:
            tool_row = conn.execute(
                "SELECT tool_item_key, action_key, required_level "
                "FROM v_tool_progression WHERE action_key = 'mine_iron_vein'"
            ).fetchone()
            sink_types = {
                row[0]
                for row in conn.execute(
                    "SELECT sink_type FROM item_sinks WHERE item_key = 'bronze_pick'"
                )
            }
        self.assertEqual(tuple(tool_row), ("bronze_pick", "mine_iron_vein", 5))
        self.assertIn("tool_use", sink_types)
        self.assertIn("equipment_use", sink_types)

    def test_item_can_have_multiple_sources_and_sinks(self) -> None:
        with self.database() as conn:
            row = conn.execute(
                "SELECT source_count, sink_count, source_type_count, sink_type_count "
                "FROM item_metrics WHERE item_key = 'iron_bar'"
            ).fetchone()
        self.assertEqual(tuple(row), (2, 2, 2, 2))

    def test_calculator_contract_is_deterministic(self) -> None:
        config = balance_config()
        validate_config(config)
        first = derive_action_math(config, "mining", 1, "gathering")
        second = derive_action_math(copy.deepcopy(config), "mining", 1, "gathering")
        self.assertEqual(first, second)
        self.assertEqual(first["target_xp_per_hour"], 3_600.0)
        self.assertEqual(first["xp_per_action"], 20.0)

    def test_build_is_deterministic_for_same_inputs(self) -> None:
        other_db = self.temp_root / "second.sqlite"
        with contextlib.redirect_stdout(io.StringIO()):
            build(self.input_dir, other_db, SCHEMA_PATH, self.config_path, None)
        with self.database() as left, contextlib.closing(sqlite3.connect(other_db)) as right:
            for table, order_by in (
                ("metadata", "key"),
                ("gathering_action_outputs", "action_key, item_key, mode"),
                ("item_metrics", "item_key"),
                ("validation_findings", "finding_id"),
            ):
                left_rows = [
                    tuple(row)
                    for row in left.execute(f"SELECT * FROM {table} ORDER BY {order_by}")
                ]
                right_rows = right.execute(
                    f"SELECT * FROM {table} ORDER BY {order_by}"
                ).fetchall()
                self.assertEqual(left_rows, right_rows)

    def test_invalid_item_reference_is_rejected_before_db_write(self) -> None:
        batch = valid_batch()
        batch["recipes"][0]["inputs"][0]["item_key"] = "missing_ore"
        semantic_validate_batch(batch, Path("invalid_reference.json"))
        merged = merge_batches([(Path("invalid_reference.json"), batch)])
        with self.assertRaisesRegex(ContentError, "missing item missing_ore"):
            cross_reference_validate(merged)

    def test_unjustified_rng_is_rejected(self) -> None:
        batch = valid_batch()
        batch["gathering_actions"][0]["outputs"][1]["rng_rationale"] = None
        with self.assertRaisesRegex(ContentError, "requires rng_rationale"):
            semantic_validate_batch(batch, Path("unjustified_rng.json"))


if __name__ == "__main__":
    unittest.main()
