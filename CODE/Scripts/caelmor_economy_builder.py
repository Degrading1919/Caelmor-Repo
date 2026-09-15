#!/usr/bin/env python3
"""
Build and validate a canonical analytical SQLite economy database from worker
interchange batches.

The builder uses stable text keys, deterministic ordering, foreign-key checks,
derived source/sink relationships, connectivity metrics, dependency depth, and
design QA findings. It does not modify Caelmor runtime C#.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import tempfile
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import jsonschema  # optional
except Exception:
    jsonschema = None

from caelmor_progression_calculator import (
    BalanceConfigError,
    band_map,
    derive_action_math,
    load_config,
    weighted_probability,
    xp_table,
)


KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")

REGIONS = ("lowmark", "thornfell", "mire", "emberholt", "cross_region")
SKILLS = (
    "foraging",
    "hunting",
    "angling",
    "mining",
    "woodcutting",
    "scavenging",
    "smithing",
    "leatherworking",
    "fletching",
    "alchemy",
    "cooking",
    "adornment",
    "mechanisms",
    "fabrication",
)
RARITIES = ("common", "uncommon", "rare", "special")
TERMINAL_ROLES = {"consumable", "equipment", "tool", "ammunition", "trade_good"}


class ContentError(ValueError):
    pass


def load_batches(input_dir: Path, schema_path: Optional[Path]) -> List[Tuple[Path, Dict[str, Any]]]:
    if not input_dir.exists():
        raise FileNotFoundError(input_dir)

    schema = None
    if schema_path:
        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)

    files = sorted(p for p in input_dir.rglob("*.json") if p.resolve() != (schema_path.resolve() if schema_path else None))
    if not files:
        raise ContentError(f"No JSON worker batches found under {input_dir}")

    batches = []
    for path in files:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if schema is not None and jsonschema is not None:
            jsonschema.validate(data, schema)

        semantic_validate_batch(data, path)
        batches.append((path, data))

    return batches


def _require_key(value: Any, field: str, path: Path) -> str:
    if not isinstance(value, str) or not KEY_RE.fullmatch(value):
        raise ContentError(f"{path}: {field} must be lowercase snake_case key")
    return value


def semantic_validate_batch(batch: Dict[str, Any], path: Path) -> None:
    expected_top = {"batch_id", "notes", "items", "gathering_actions", "gathering_nodes", "recipes"}
    extras = set(batch) - expected_top
    if extras:
        raise ContentError(f"{path}: unsupported top-level keys: {sorted(extras)}")

    for key in ("batch_id", "items", "gathering_actions", "gathering_nodes", "recipes"):
        if key not in batch:
            raise ContentError(f"{path}: missing top-level key {key}")

    _require_key(batch["batch_id"], "batch_id", path)

    for collection in ("items", "gathering_actions", "gathering_nodes", "recipes"):
        if not isinstance(batch[collection], list):
            raise ContentError(f"{path}: {collection} must be an array")

    for item in batch["items"]:
        for field in (
            "slot_id", "key", "display_name", "description", "category", "form",
            "economic_role", "purpose", "region_keys", "tags", "cross_tier_role",
            "rarity_role", "external_sources", "external_sinks",
        ):
            if field not in item:
                raise ContentError(f"{path}: item missing {field}")
        _require_key(item["slot_id"], "item.slot_id", path)
        _require_key(item["key"], "item.key", path)
        if not item["display_name"] or not item["description"] or not item["purpose"]:
            raise ContentError(f"{path}: item text fields may not be empty")
        if not isinstance(item["region_keys"], list) or not item["region_keys"]:
            raise ContentError(f"{path}: item.region_keys must be non-empty")
        if any(r not in REGIONS for r in item["region_keys"]):
            raise ContentError(f"{path}: item has invalid region")
        if item["rarity_role"] not in RARITIES:
            raise ContentError(f"{path}: item has invalid rarity_role")

    for action in batch["gathering_actions"]:
        for field in (
            "slot_id", "key", "display_name", "skill_key", "level_band",
            "purpose", "region_keys", "outputs", "tool_tags",
        ):
            if field not in action:
                raise ContentError(f"{path}: gathering action missing {field}")
        _require_key(action["slot_id"], "gathering_action.slot_id", path)
        _require_key(action["key"], "gathering_action.key", path)
        if action["skill_key"] not in SKILLS:
            raise ContentError(f"{path}: invalid gathering action skill")
        if not isinstance(action["level_band"], int) or action["level_band"] < 1:
            raise ContentError(f"{path}: action level_band must be positive integer")
        if not isinstance(action["outputs"], list) or not action["outputs"]:
            raise ContentError(f"{path}: gathering action must have outputs")
        for out in action["outputs"]:
            for field in ("item_key", "quantity", "mode", "rarity_role"):
                if field not in out:
                    raise ContentError(f"{path}: gathering output missing {field}")
            _require_key(out["item_key"], "gathering_output.item_key", path)
            if out["mode"] not in {"guaranteed", "weighted", "conditional"}:
                raise ContentError(f"{path}: invalid gathering output mode")
            if out["rarity_role"] not in RARITIES:
                raise ContentError(f"{path}: invalid gathering output rarity")

    for node in batch["gathering_nodes"]:
        for field in (
            "slot_id", "key", "display_name", "action_key", "region_key",
            "world_context", "interaction_verb", "depletable", "respawnable", "stateful",
        ):
            if field not in node:
                raise ContentError(f"{path}: gathering node missing {field}")
        _require_key(node["slot_id"], "gathering_node.slot_id", path)
        _require_key(node["key"], "gathering_node.key", path)
        _require_key(node["action_key"], "gathering_node.action_key", path)
        if node["region_key"] not in REGIONS:
            raise ContentError(f"{path}: gathering node has invalid region")

    for recipe in batch["recipes"]:
        for field in (
            "slot_id", "key", "display_name", "skill_key", "level_band",
            "purpose", "region_keys", "inputs", "outputs", "cross_skill_links",
        ):
            if field not in recipe:
                raise ContentError(f"{path}: recipe missing {field}")
        _require_key(recipe["slot_id"], "recipe.slot_id", path)
        _require_key(recipe["key"], "recipe.key", path)
        if recipe["skill_key"] not in SKILLS:
            raise ContentError(f"{path}: invalid recipe skill")
        if not isinstance(recipe["inputs"], list) or not recipe["inputs"]:
            raise ContentError(f"{path}: recipe must have inputs")
        if not isinstance(recipe["outputs"], list) or not recipe["outputs"]:
            raise ContentError(f"{path}: recipe must have outputs")
        for io_group in ("inputs", "outputs"):
            for io in recipe[io_group]:
                _require_key(io.get("item_key"), f"recipe.{io_group}.item_key", path)
                if not isinstance(io.get("quantity"), int) or io["quantity"] < 1:
                    raise ContentError(f"{path}: recipe quantities must be positive integers")


def merge_batches(batches: List[Tuple[Path, Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    merged = {
        "items": [],
        "gathering_actions": [],
        "gathering_nodes": [],
        "recipes": [],
    }
    seen: Dict[str, Dict[str, Path]] = {k: {} for k in merged}

    for path, batch in batches:
        for collection in merged:
            for record in batch[collection]:
                key = record["key"]
                if key in seen[collection]:
                    raise ContentError(
                        f"Duplicate {collection} key {key!r} in {path} and {seen[collection][key]}"
                    )
                seen[collection][key] = path
                copy = dict(record)
                copy["_source_batch"] = batch["batch_id"]
                copy["_source_file"] = str(path)
                merged[collection].append(copy)

    for collection in merged:
        merged[collection].sort(key=lambda r: r["key"])

    return merged


def cross_reference_validate(data: Dict[str, List[Dict[str, Any]]]) -> None:
    items = {r["key"] for r in data["items"]}
    actions = {r["key"] for r in data["gathering_actions"]}

    errors = []

    for action in data["gathering_actions"]:
        for out in action["outputs"]:
            if out["item_key"] not in items:
                errors.append(f"Action {action['key']} references missing item {out['item_key']}")

    for node in data["gathering_nodes"]:
        if node["action_key"] not in actions:
            errors.append(f"Node {node['key']} references missing action {node['action_key']}")

    for recipe in data["recipes"]:
        for io_group in ("inputs", "outputs"):
            for io in recipe[io_group]:
                if io["item_key"] not in items:
                    errors.append(
                        f"Recipe {recipe['key']} {io_group} references missing item {io['item_key']}"
                    )

    if errors:
        raise ContentError("Cross-reference validation failed:\n- " + "\n- ".join(errors))


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE regions (
            region_key TEXT PRIMARY KEY
        );

        CREATE TABLE skills (
            skill_key TEXT PRIMARY KEY
        );

        CREATE TABLE progression_bands (
            band_id INTEGER PRIMARY KEY,
            level_min INTEGER NOT NULL,
            level_max INTEGER NOT NULL,
            target_xp_per_hour REAL,
            gather_action_seconds REAL,
            craft_action_seconds REAL,
            gather_success_chance REAL,
            weighted_bonus_roll_chance REAL
        );

        CREATE TABLE xp_levels (
            level INTEGER PRIMARY KEY,
            total_xp INTEGER NOT NULL,
            xp_to_next INTEGER
        );

        CREATE TABLE items (
            item_key TEXT PRIMARY KEY,
            slot_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            form TEXT NOT NULL,
            economic_role TEXT NOT NULL,
            purpose TEXT NOT NULL,
            cross_tier_role TEXT NOT NULL,
            rarity_role TEXT NOT NULL,
            notes TEXT,
            source_batch TEXT NOT NULL,
            source_file TEXT NOT NULL
        );

        CREATE TABLE item_regions (
            item_key TEXT NOT NULL REFERENCES items(item_key),
            region_key TEXT NOT NULL REFERENCES regions(region_key),
            PRIMARY KEY (item_key, region_key)
        );

        CREATE TABLE item_tags (
            item_key TEXT NOT NULL REFERENCES items(item_key),
            tag TEXT NOT NULL,
            PRIMARY KEY (item_key, tag)
        );

        CREATE TABLE gathering_actions (
            action_key TEXT PRIMARY KEY,
            slot_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            skill_key TEXT NOT NULL REFERENCES skills(skill_key),
            level_band INTEGER NOT NULL,
            purpose TEXT NOT NULL,
            action_seconds REAL,
            success_chance REAL,
            target_xp_per_hour REAL,
            xp_per_action REAL,
            attempts_per_hour REAL,
            notes TEXT,
            source_batch TEXT NOT NULL,
            source_file TEXT NOT NULL
        );

        CREATE TABLE gathering_action_regions (
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            region_key TEXT NOT NULL REFERENCES regions(region_key),
            PRIMARY KEY (action_key, region_key)
        );

        CREATE TABLE gathering_action_tools (
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            tool_tag TEXT NOT NULL,
            PRIMARY KEY (action_key, tool_tag)
        );

        CREATE TABLE gathering_action_outputs (
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            item_key TEXT NOT NULL REFERENCES items(item_key),
            quantity INTEGER NOT NULL,
            mode TEXT NOT NULL,
            rarity_role TEXT NOT NULL,
            condition_tag TEXT,
            relative_weight REAL,
            output_probability REAL,
            expected_quantity_per_hour REAL,
            PRIMARY KEY (action_key, item_key, mode, rarity_role, condition_tag)
        );

        CREATE TABLE gathering_nodes (
            node_key TEXT PRIMARY KEY,
            slot_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            region_key TEXT NOT NULL REFERENCES regions(region_key),
            world_context TEXT NOT NULL,
            interaction_verb TEXT NOT NULL,
            depletable INTEGER NOT NULL,
            respawnable INTEGER NOT NULL,
            stateful INTEGER NOT NULL,
            notes TEXT,
            source_batch TEXT NOT NULL,
            source_file TEXT NOT NULL
        );

        CREATE TABLE recipes (
            recipe_key TEXT PRIMARY KEY,
            slot_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            skill_key TEXT NOT NULL REFERENCES skills(skill_key),
            level_band INTEGER NOT NULL,
            purpose TEXT NOT NULL,
            station_tag TEXT,
            action_seconds REAL,
            target_xp_per_hour REAL,
            xp_per_action REAL,
            attempts_per_hour REAL,
            notes TEXT,
            source_batch TEXT NOT NULL,
            source_file TEXT NOT NULL
        );

        CREATE TABLE recipe_regions (
            recipe_key TEXT NOT NULL REFERENCES recipes(recipe_key),
            region_key TEXT NOT NULL REFERENCES regions(region_key),
            PRIMARY KEY (recipe_key, region_key)
        );

        CREATE TABLE recipe_cross_skills (
            recipe_key TEXT NOT NULL REFERENCES recipes(recipe_key),
            skill_key TEXT NOT NULL REFERENCES skills(skill_key),
            PRIMARY KEY (recipe_key, skill_key)
        );

        CREATE TABLE recipe_inputs (
            recipe_key TEXT NOT NULL REFERENCES recipes(recipe_key),
            item_key TEXT NOT NULL REFERENCES items(item_key),
            quantity INTEGER NOT NULL,
            PRIMARY KEY (recipe_key, item_key)
        );

        CREATE TABLE recipe_outputs (
            recipe_key TEXT NOT NULL REFERENCES recipes(recipe_key),
            item_key TEXT NOT NULL REFERENCES items(item_key),
            quantity INTEGER NOT NULL,
            PRIMARY KEY (recipe_key, item_key)
        );

        CREATE TABLE item_sources (
            item_key TEXT NOT NULL REFERENCES items(item_key),
            source_type TEXT NOT NULL,
            source_key TEXT NOT NULL,
            detail TEXT,
            level_band INTEGER,
            skill_key TEXT,
            PRIMARY KEY (item_key, source_type, source_key)
        );

        CREATE TABLE item_sinks (
            item_key TEXT NOT NULL REFERENCES items(item_key),
            sink_type TEXT NOT NULL,
            sink_key TEXT NOT NULL,
            detail TEXT,
            level_band INTEGER,
            skill_key TEXT,
            PRIMARY KEY (item_key, sink_type, sink_key)
        );

        CREATE TABLE item_metrics (
            item_key TEXT PRIMARY KEY REFERENCES items(item_key),
            source_count INTEGER NOT NULL,
            sink_count INTEGER NOT NULL,
            source_type_count INTEGER NOT NULL,
            sink_type_count INTEGER NOT NULL,
            skills_connected INTEGER NOT NULL,
            regions_connected INTEGER NOT NULL,
            earliest_source_band INTEGER,
            latest_sink_band INTEGER,
            progression_band_span INTEGER,
            dependency_depth INTEGER,
            cross_tier_reuse_count INTEGER NOT NULL
        );

        CREATE TABLE skill_metrics (
            skill_key TEXT PRIMARY KEY REFERENCES skills(skill_key),
            gathering_action_count INTEGER NOT NULL,
            recipe_count INTEGER NOT NULL,
            distinct_item_count INTEGER NOT NULL,
            covered_band_count INTEGER NOT NULL
        );

        CREATE TABLE validation_findings (
            finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity TEXT NOT NULL,
            finding_type TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_key TEXT NOT NULL,
            detail TEXT NOT NULL
        );

        CREATE INDEX idx_sources_item ON item_sources(item_key);
        CREATE INDEX idx_sinks_item ON item_sinks(item_key);
        CREATE INDEX idx_actions_skill_band ON gathering_actions(skill_key, level_band);
        CREATE INDEX idx_recipes_skill_band ON recipes(skill_key, level_band);
        CREATE INDEX idx_nodes_action ON gathering_nodes(action_key);
        """
    )


def seed_reference_tables(conn: sqlite3.Connection) -> None:
    conn.executemany("INSERT INTO regions(region_key) VALUES (?)", [(r,) for r in REGIONS])
    conn.executemany("INSERT INTO skills(skill_key) VALUES (?)", [(s,) for s in SKILLS])


def insert_progression(conn: sqlite3.Connection, cfg: Optional[Dict[str, Any]]) -> None:
    if cfg is None:
        return

    conn.execute("INSERT INTO metadata(key, value) VALUES (?, ?)", ("balance_status", str(cfg["status"])))

    for band in cfg["bands"]:
        conn.execute(
            """
            INSERT INTO progression_bands(
                band_id, level_min, level_max, target_xp_per_hour,
                gather_action_seconds, craft_action_seconds,
                gather_success_chance, weighted_bonus_roll_chance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                band["id"], band["level_min"], band["level_max"], band["target_xp_per_hour"],
                band["gather_action_seconds"], band["craft_action_seconds"],
                band["gather_success_chance"], band["weighted_bonus_roll_chance"],
            ),
        )

    for row in xp_table(cfg):
        conn.execute(
            "INSERT INTO xp_levels(level, total_xp, xp_to_next) VALUES (?, ?, ?)",
            (row["level"], row["total_xp"], row["xp_to_next"]),
        )


def insert_content(
    conn: sqlite3.Connection,
    data: Dict[str, List[Dict[str, Any]]],
    cfg: Optional[Dict[str, Any]],
) -> None:
    for item in data["items"]:
        conn.execute(
            """
            INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["key"], item["slot_id"], item["display_name"], item["description"],
                item["category"], item["form"], item["economic_role"], item["purpose"],
                item["cross_tier_role"], item["rarity_role"], item.get("notes"),
                item["_source_batch"], item["_source_file"],
            ),
        )
        for region in sorted(set(item["region_keys"])):
            conn.execute("INSERT INTO item_regions VALUES (?, ?)", (item["key"], region))
        for tag in sorted(set(item.get("tags", []))):
            conn.execute("INSERT INTO item_tags VALUES (?, ?)", (item["key"], tag))

    for action in data["gathering_actions"]:
        math = None
        if cfg is not None:
            math = derive_action_math(cfg, action["skill_key"], action["level_band"], "gathering")

        conn.execute(
            """
            INSERT INTO gathering_actions(
                action_key, slot_id, display_name, description, skill_key, level_band, purpose,
                action_seconds, success_chance, target_xp_per_hour, xp_per_action,
                attempts_per_hour, notes, source_batch, source_file
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                action["key"], action["slot_id"], action["display_name"], action.get("description"),
                action["skill_key"], action["level_band"], action["purpose"],
                None if math is None else math["action_seconds"],
                None if math is None else math["success_chance"],
                None if math is None else math["target_xp_per_hour"],
                None if math is None else math["xp_per_action"],
                None if math is None else math["attempts_per_hour"],
                action.get("notes"), action["_source_batch"], action["_source_file"],
            ),
        )

        for region in sorted(set(action["region_keys"])):
            conn.execute("INSERT INTO gathering_action_regions VALUES (?, ?)", (action["key"], region))
        for tool in sorted(set(action.get("tool_tags", []))):
            conn.execute("INSERT INTO gathering_action_tools VALUES (?, ?)", (action["key"], tool))

        weighted = [o for o in action["outputs"] if o["mode"] == "weighted"]
        for out in action["outputs"]:
            relative_weight = None
            probability = None
            expected_per_hour = None

            if cfg is not None and math is not None:
                if out["mode"] == "guaranteed":
                    probability = math["success_chance"]
                elif out["mode"] == "weighted":
                    relative_weight = float(cfg["rarity_weights"][out["rarity_role"]])
                    probability = (
                        math["success_chance"]
                        * weighted_probability(
                            cfg,
                            action["level_band"],
                            out["rarity_role"],
                            weighted,
                        )
                    )
                if probability is not None:
                    expected_per_hour = (
                        math["attempts_per_hour"] * probability * int(out["quantity"])
                    )

            conn.execute(
                """
                INSERT INTO gathering_action_outputs(
                    action_key, item_key, quantity, mode, rarity_role, condition_tag,
                    relative_weight, output_probability, expected_quantity_per_hour
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    action["key"], out["item_key"], out["quantity"], out["mode"],
                    out["rarity_role"], out.get("condition_tag"), relative_weight,
                    probability, expected_per_hour,
                ),
            )

    for node in data["gathering_nodes"]:
        conn.execute(
            """
            INSERT INTO gathering_nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                node["key"], node["slot_id"], node["display_name"], node.get("description"),
                node["action_key"], node["region_key"], node["world_context"],
                node["interaction_verb"], int(bool(node["depletable"])),
                int(bool(node["respawnable"])), int(bool(node["stateful"])),
                node.get("notes"), node["_source_batch"], node["_source_file"],
            ),
        )

    for recipe in data["recipes"]:
        math = None
        if cfg is not None:
            math = derive_action_math(cfg, recipe["skill_key"], recipe["level_band"], "crafting")

        conn.execute(
            """
            INSERT INTO recipes(
                recipe_key, slot_id, display_name, description, skill_key, level_band, purpose,
                station_tag, action_seconds, target_xp_per_hour, xp_per_action,
                attempts_per_hour, notes, source_batch, source_file
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recipe["key"], recipe["slot_id"], recipe["display_name"], recipe.get("description"),
                recipe["skill_key"], recipe["level_band"], recipe["purpose"],
                recipe.get("station_tag"),
                None if math is None else math["action_seconds"],
                None if math is None else math["target_xp_per_hour"],
                None if math is None else math["xp_per_action"],
                None if math is None else math["attempts_per_hour"],
                recipe.get("notes"), recipe["_source_batch"], recipe["_source_file"],
            ),
        )

        for region in sorted(set(recipe["region_keys"])):
            conn.execute("INSERT INTO recipe_regions VALUES (?, ?)", (recipe["key"], region))
        for skill in sorted(set(recipe.get("cross_skill_links", []))):
            conn.execute("INSERT INTO recipe_cross_skills VALUES (?, ?)", (recipe["key"], skill))
        for io in recipe["inputs"]:
            conn.execute(
                "INSERT INTO recipe_inputs VALUES (?, ?, ?)",
                (recipe["key"], io["item_key"], io["quantity"]),
            )
        for io in recipe["outputs"]:
            conn.execute(
                "INSERT INTO recipe_outputs VALUES (?, ?, ?)",
                (recipe["key"], io["item_key"], io["quantity"]),
            )


def build_sources_and_sinks(
    conn: sqlite3.Connection,
    data: Dict[str, List[Dict[str, Any]]],
) -> None:
    for action_key, item_key, level_band, skill_key in conn.execute(
        """
        SELECT gao.action_key, gao.item_key, ga.level_band, ga.skill_key
        FROM gathering_action_outputs gao
        JOIN gathering_actions ga ON ga.action_key = gao.action_key
        """
    ):
        conn.execute(
            """
            INSERT INTO item_sources(item_key, source_type, source_key, detail, level_band, skill_key)
            VALUES (?, 'gathering', ?, NULL, ?, ?)
            """,
            (item_key, action_key, level_band, skill_key),
        )

    for recipe_key, item_key, level_band, skill_key in conn.execute(
        """
        SELECT ro.recipe_key, ro.item_key, r.level_band, r.skill_key
        FROM recipe_outputs ro
        JOIN recipes r ON r.recipe_key = ro.recipe_key
        """
    ):
        conn.execute(
            """
            INSERT INTO item_sources(item_key, source_type, source_key, detail, level_band, skill_key)
            VALUES (?, 'recipe', ?, NULL, ?, ?)
            """,
            (item_key, recipe_key, level_band, skill_key),
        )

    for recipe_key, item_key, level_band, skill_key in conn.execute(
        """
        SELECT ri.recipe_key, ri.item_key, r.level_band, r.skill_key
        FROM recipe_inputs ri
        JOIN recipes r ON r.recipe_key = ri.recipe_key
        """
    ):
        conn.execute(
            """
            INSERT INTO item_sinks(item_key, sink_type, sink_key, detail, level_band, skill_key)
            VALUES (?, 'recipe', ?, NULL, ?, ?)
            """,
            (item_key, recipe_key, level_band, skill_key),
        )

    item_records = {r["key"]: r for r in data["items"]}
    for item_key, item in item_records.items():
        for i, rel in enumerate(item.get("external_sources", []), 1):
            source_key = f"{rel['relation_type']}:{i}:{item_key}"
            conn.execute(
                """
                INSERT INTO item_sources(item_key, source_type, source_key, detail, level_band, skill_key)
                VALUES (?, ?, ?, ?, NULL, NULL)
                """,
                (item_key, rel["relation_type"], source_key, rel["detail"]),
            )
        for i, rel in enumerate(item.get("external_sinks", []), 1):
            sink_key = f"{rel['relation_type']}:{i}:{item_key}"
            conn.execute(
                """
                INSERT INTO item_sinks(item_key, sink_type, sink_key, detail, level_band, skill_key)
                VALUES (?, ?, ?, ?, NULL, NULL)
                """,
                (item_key, rel["relation_type"], sink_key, rel["detail"]),
            )


def recipe_dependency_depths(conn: sqlite3.Connection) -> Tuple[Dict[str, int], Set[str]]:
    items = [r[0] for r in conn.execute("SELECT item_key FROM items ORDER BY item_key")]
    predecessors: Dict[str, Set[str]] = defaultdict(set)
    successors: Dict[str, Set[str]] = defaultdict(set)

    for recipe_key, input_item in conn.execute("SELECT recipe_key, item_key FROM recipe_inputs"):
        for (output_item,) in conn.execute(
            "SELECT item_key FROM recipe_outputs WHERE recipe_key = ?", (recipe_key,)
        ):
            if input_item != output_item:
                successors[input_item].add(output_item)
                predecessors[output_item].add(input_item)

    indegree = {item: len(predecessors[item]) for item in items}
    q = deque(sorted(item for item in items if indegree[item] == 0))
    depth = {item: 0 for item in items}
    visited = 0

    while q:
        item = q.popleft()
        visited += 1
        for nxt in sorted(successors[item]):
            depth[nxt] = max(depth[nxt], depth[item] + 1)
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    cyclic = {item for item, deg in indegree.items() if deg > 0}
    for item in cyclic:
        depth[item] = -1

    return depth, cyclic


def calculate_metrics_and_findings(
    conn: sqlite3.Connection,
    data: Dict[str, List[Dict[str, Any]]],
    cfg: Optional[Dict[str, Any]],
) -> None:
    item_map = {r["key"]: r for r in data["items"]}
    depth, cyclic = recipe_dependency_depths(conn)

    for item_key in sorted(item_map):
        source_count = conn.execute(
            "SELECT COUNT(*) FROM item_sources WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        sink_count = conn.execute(
            "SELECT COUNT(*) FROM item_sinks WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        source_type_count = conn.execute(
            "SELECT COUNT(DISTINCT source_type) FROM item_sources WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        sink_type_count = conn.execute(
            "SELECT COUNT(DISTINCT sink_type) FROM item_sinks WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        skills_connected = conn.execute(
            """
            SELECT COUNT(DISTINCT skill_key) FROM (
                SELECT skill_key FROM item_sources WHERE item_key = ? AND skill_key IS NOT NULL
                UNION
                SELECT skill_key FROM item_sinks WHERE item_key = ? AND skill_key IS NOT NULL
            )
            """,
            (item_key, item_key),
        ).fetchone()[0]
        regions_connected = conn.execute(
            "SELECT COUNT(*) FROM item_regions WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        earliest_source_band = conn.execute(
            "SELECT MIN(level_band) FROM item_sources WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        latest_sink_band = conn.execute(
            "SELECT MAX(level_band) FROM item_sinks WHERE item_key = ?", (item_key,)
        ).fetchone()[0]

        span = None
        cross_tier_reuse = 0
        if earliest_source_band is not None and latest_sink_band is not None:
            span = int(latest_sink_band) - int(earliest_source_band)
            cross_tier_reuse = conn.execute(
                """
                SELECT COUNT(*)
                FROM item_sinks
                WHERE item_key = ?
                  AND level_band IS NOT NULL
                  AND level_band >= ?
                """,
                (item_key, int(earliest_source_band) + 2),
            ).fetchone()[0]

        conn.execute(
            """
            INSERT INTO item_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_key, source_count, sink_count, source_type_count, sink_type_count,
                skills_connected, regions_connected, earliest_source_band, latest_sink_band,
                span, depth.get(item_key, 0), cross_tier_reuse,
            ),
        )

        item = item_map[item_key]
        if source_count == 0:
            add_finding(
                conn, "error", "orphan_source", "item", item_key,
                "Item has no modeled acquisition source."
            )

        if sink_count == 0 and item["economic_role"] not in TERMINAL_ROLES:
            add_finding(
                conn, "error", "dead_end_item", "item", item_key,
                f"Non-terminal {item['economic_role']} has no modeled sink."
            )

        if item["cross_tier_role"] == "persistent" and cross_tier_reuse == 0:
            add_finding(
                conn, "warning", "cross_tier_contract_unmet", "item", item_key,
                "Item is marked persistent but has no modeled sink at least two bands after its earliest source."
            )

        if item_key in cyclic:
            add_finding(
                conn, "error", "recipe_cycle", "item", item_key,
                "Item participates in a recipe dependency cycle; dependency depth is set to -1."
            )

    for skill in SKILLS:
        gather_count = conn.execute(
            "SELECT COUNT(*) FROM gathering_actions WHERE skill_key = ?", (skill,)
        ).fetchone()[0]
        recipe_count = conn.execute(
            "SELECT COUNT(*) FROM recipes WHERE skill_key = ?", (skill,)
        ).fetchone()[0]
        distinct_item_count = conn.execute(
            """
            SELECT COUNT(DISTINCT item_key) FROM (
                SELECT gao.item_key
                FROM gathering_action_outputs gao
                JOIN gathering_actions ga ON ga.action_key = gao.action_key
                WHERE ga.skill_key = ?
                UNION
                SELECT ri.item_key
                FROM recipe_inputs ri
                JOIN recipes r ON r.recipe_key = ri.recipe_key
                WHERE r.skill_key = ?
                UNION
                SELECT ro.item_key
                FROM recipe_outputs ro
                JOIN recipes r ON r.recipe_key = ro.recipe_key
                WHERE r.skill_key = ?
            )
            """,
            (skill, skill, skill),
        ).fetchone()[0]
        covered_band_count = conn.execute(
            """
            SELECT COUNT(DISTINCT level_band) FROM (
                SELECT level_band FROM gathering_actions WHERE skill_key = ?
                UNION
                SELECT level_band FROM recipes WHERE skill_key = ?
            )
            """,
            (skill, skill),
        ).fetchone()[0]

        conn.execute(
            "INSERT INTO skill_metrics VALUES (?, ?, ?, ?, ?)",
            (skill, gather_count, recipe_count, distinct_item_count, covered_band_count),
        )

    if cfg is not None:
        band_ids = [int(b["id"]) for b in cfg["bands"]]
        for skill in SKILLS:
            if conn.execute(
                "SELECT COUNT(*) FROM gathering_actions WHERE skill_key = ?", (skill,)
            ).fetchone()[0] == 0 and conn.execute(
                "SELECT COUNT(*) FROM recipes WHERE skill_key = ?", (skill,)
            ).fetchone()[0] == 0:
                continue

            covered = {
                r[0] for r in conn.execute(
                    """
                    SELECT level_band FROM gathering_actions WHERE skill_key = ?
                    UNION
                    SELECT level_band FROM recipes WHERE skill_key = ?
                    """,
                    (skill, skill),
                )
            }
            for band_id in band_ids:
                if band_id not in covered:
                    add_finding(
                        conn, "warning", "progression_gap", "skill", skill,
                        f"No gathering action or recipe is modeled in progression band {band_id}."
                    )

    # Potential redundancy: same role/category/form with same earliest band and no distinct tags.
    signatures: Dict[Tuple[Any, ...], List[str]] = defaultdict(list)
    for item in data["items"]:
        earliest = conn.execute(
            "SELECT earliest_source_band FROM item_metrics WHERE item_key = ?", (item["key"],)
        ).fetchone()[0]
        signature = (
            item["category"],
            item["form"],
            item["economic_role"],
            earliest,
            tuple(sorted(item.get("tags", []))),
        )
        signatures[signature].append(item["key"])

    for signature, keys in signatures.items():
        if len(keys) >= 3:
            for key in keys:
                add_finding(
                    conn, "info", "potential_redundancy", "item", key,
                    f"Shares a structural signature with {len(keys)-1} other items: {', '.join(k for k in keys if k != key)}"
                )


def add_finding(
    conn: sqlite3.Connection,
    severity: str,
    finding_type: str,
    entity_type: str,
    entity_key: str,
    detail: str,
) -> None:
    conn.execute(
        """
        INSERT INTO validation_findings(severity, finding_type, entity_type, entity_key, detail)
        VALUES (?, ?, ?, ?, ?)
        """,
        (severity, finding_type, entity_type, entity_key, detail),
    )


def report(conn: sqlite3.Connection) -> str:
    counts = {}
    for table in (
        "items", "gathering_actions", "gathering_nodes", "gathering_action_outputs",
        "recipes", "recipe_inputs", "recipe_outputs", "item_sources", "item_sinks",
        "validation_findings",
    ):
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    severities = dict(
        conn.execute(
            "SELECT severity, COUNT(*) FROM validation_findings GROUP BY severity"
        ).fetchall()
    )

    top_connected = conn.execute(
        """
        SELECT i.item_key, i.display_name, m.source_count, m.sink_count,
               m.skills_connected, m.progression_band_span
        FROM item_metrics m
        JOIN items i ON i.item_key = m.item_key
        ORDER BY (m.source_count + m.sink_count) DESC, i.item_key
        LIMIT 15
        """
    ).fetchall()

    lines = [
        "Caelmor Economy Database Audit",
        "==============================",
        "",
        "Row counts",
        "----------",
    ]
    for table, count in counts.items():
        lines.append(f"{table:<28} {count:,}")

    lines += [
        "",
        "Validation findings",
        "-------------------",
        f"errors   {severities.get('error', 0):,}",
        f"warnings {severities.get('warning', 0):,}",
        f"info     {severities.get('info', 0):,}",
        "",
        "Most connected items",
        "--------------------",
    ]
    for row in top_connected:
        lines.append(
            f"{row[0]} | {row[1]} | sources={row[2]} sinks={row[3]} "
            f"skills={row[4]} band_span={row[5]}"
        )

    return "\n".join(lines)


def build(
    input_dir: Path,
    output_db: Path,
    schema_path: Optional[Path],
    progression_config: Optional[Path],
    audit_path: Optional[Path],
) -> None:
    batches = load_batches(input_dir, schema_path)
    data = merge_batches(batches)
    cross_reference_validate(data)

    cfg = None
    if progression_config is not None:
        cfg = load_config(progression_config)

        valid_band_ids = set(band_map(cfg))
        for collection in ("gathering_actions", "recipes"):
            for record in data[collection]:
                if record["level_band"] not in valid_band_ids:
                    raise ContentError(
                        f"{collection} {record['key']} uses level_band {record['level_band']} "
                        "which does not exist in the progression config"
                    )

    output_db.parent.mkdir(parents=True, exist_ok=True)
    if output_db.exists():
        output_db.unlink()

    conn = connect(output_db)
    try:
        create_schema(conn)
        seed_reference_tables(conn)
        insert_progression(conn, cfg)
        insert_content(conn, data, cfg)
        build_sources_and_sinks(conn, data)
        calculate_metrics_and_findings(conn, data, cfg)

        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
        if fk_errors:
            raise ContentError(f"SQLite foreign key check failed: {fk_errors}")

        conn.commit()
        text = report(conn)
    except Exception:
        conn.rollback()
        conn.close()
        if output_db.exists():
            output_db.unlink()
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if audit_path:
        audit_path.write_text(text, encoding="utf-8")
    print(text)
    print()
    print(f"Database: {output_db}")
    if audit_path:
        print(f"Audit:    {audit_path}")


def write_self_test_batch(path: Path) -> None:
    sample = {
        "batch_id": "self_test",
        "notes": "Generated by --self-test.",
        "items": [
            {
                "slot_id": "iron_ore_slot",
                "key": "iron_ore",
                "display_name": "Iron Ore",
                "description": "A workable iron-bearing ore.",
                "category": "core_structures",
                "form": "raw",
                "economic_role": "raw_material",
                "purpose": "Early metal progression input.",
                "region_keys": ["lowmark"],
                "tags": ["metal", "iron"],
                "cross_tier_role": "persistent",
                "rarity_role": "common",
                "external_sources": [],
                "external_sinks": [],
                "notes": None
            },
            {
                "slot_id": "iron_bar_slot",
                "key": "iron_bar",
                "display_name": "Iron Bar",
                "description": "Refined iron ready for fabrication.",
                "category": "core_structures",
                "form": "processed",
                "economic_role": "component",
                "purpose": "Metal component for tools and equipment.",
                "region_keys": ["lowmark"],
                "tags": ["metal", "iron"],
                "cross_tier_role": "persistent",
                "rarity_role": "common",
                "external_sources": [],
                "external_sinks": [],
                "notes": None
            },
            {
                "slot_id": "iron_knife_slot",
                "key": "iron_knife",
                "display_name": "Iron Knife",
                "description": "A simple iron field knife.",
                "category": "core_structures",
                "form": "finished",
                "economic_role": "tool",
                "purpose": "Basic utility tool.",
                "region_keys": ["lowmark"],
                "tags": ["metal", "tool"],
                "cross_tier_role": "limited",
                "rarity_role": "common",
                "external_sources": [],
                "external_sinks": [
                    {"relation_type": "tool_use", "detail": "Used as a field cutting tool."}
                ],
                "notes": None
            }
        ],
        "gathering_actions": [
            {
                "slot_id": "mine_iron_slot",
                "key": "mine_iron_ore",
                "display_name": "Mine Iron Ore",
                "description": "Extract iron-bearing stone.",
                "skill_key": "mining",
                "level_band": 1,
                "purpose": "Core early Mining progression.",
                "region_keys": ["lowmark"],
                "outputs": [
                    {
                        "item_key": "iron_ore",
                        "quantity": 1,
                        "mode": "guaranteed",
                        "rarity_role": "common",
                        "condition_tag": None
                    }
                ],
                "tool_tags": ["pick"],
                "notes": None
            }
        ],
        "gathering_nodes": [
            {
                "slot_id": "iron_outcrop_slot",
                "key": "lowmark_iron_outcrop",
                "display_name": "Iron-Bearing Outcrop",
                "description": "A shallow weathered iron outcrop.",
                "action_key": "mine_iron_ore",
                "region_key": "lowmark",
                "world_context": "Weathered roadside quarry",
                "interaction_verb": "Mine",
                "depletable": True,
                "respawnable": True,
                "stateful": True,
                "notes": None
            }
        ],
        "recipes": [
            {
                "slot_id": "smelt_iron_slot",
                "key": "smelt_iron_bar",
                "display_name": "Smelt Iron Bar",
                "description": "Refine ore into workable iron.",
                "skill_key": "smithing",
                "level_band": 1,
                "purpose": "Primary iron refinement step.",
                "region_keys": ["lowmark"],
                "inputs": [{"item_key": "iron_ore", "quantity": 1}],
                "outputs": [{"item_key": "iron_bar", "quantity": 1}],
                "station_tag": "furnace",
                "cross_skill_links": ["mining"],
                "notes": None
            },
            {
                "slot_id": "forge_knife_slot",
                "key": "forge_iron_knife",
                "display_name": "Forge Iron Knife",
                "description": "Forge a practical iron knife.",
                "skill_key": "smithing",
                "level_band": 3,
                "purpose": "Keeps early iron relevant beyond its first band.",
                "region_keys": ["lowmark"],
                "inputs": [{"item_key": "iron_bar", "quantity": 1}],
                "outputs": [{"item_key": "iron_knife", "quantity": 1}],
                "station_tag": "anvil",
                "cross_skill_links": ["mining"],
                "notes": None
            }
        ]
    }
    path.write_text(json.dumps(sample, indent=2), encoding="utf-8")


def self_test(script_dir: Path) -> None:
    from caelmor_progression_calculator import write_template

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        batches = td / "batches"
        batches.mkdir()
        batch = batches / "self_test.json"
        write_self_test_batch(batch)

        cfg_path = td / "progression.json"
        write_template(cfg_path)

        db = td / "test.sqlite"
        audit = td / "audit.txt"
        schema = script_dir / "caelmor_worker_interchange.schema.json"

        build(batches, db, schema if schema.exists() else None, cfg_path, audit)

        conn = connect(db)
        try:
            assert conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 3
            assert conn.execute("SELECT COUNT(*) FROM gathering_actions").fetchone()[0] == 1
            assert conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 2
            assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        finally:
            conn.close()

    print("SELF-TEST PASSED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Directory containing worker batch JSON files.")
    parser.add_argument("--output", type=Path, help="Output SQLite database.")
    parser.add_argument("--schema", type=Path, help="Worker interchange JSON schema.")
    parser.add_argument("--progression-config", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test(Path(__file__).resolve().parent)
        return

    if not args.input or not args.output:
        parser.error("--input and --output are required unless --self-test is used")

    build(
        input_dir=args.input,
        output_db=args.output,
        schema_path=args.schema,
        progression_config=args.progression_config,
        audit_path=args.audit,
    )


if __name__ == "__main__":
    main()
