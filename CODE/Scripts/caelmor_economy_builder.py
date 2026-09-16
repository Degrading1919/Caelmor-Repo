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
import hashlib
import json
import re
import sqlite3
import sys
import tempfile
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import jsonschema
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
V1_CORE_SKILLS = frozenset(
    {"mining", "woodcutting", "hunting", "smithing", "fletching", "cooking", "leatherworking"}
)
GATHERING_SKILLS = frozenset(
    {"foraging", "hunting", "angling", "mining", "woodcutting", "scavenging"}
)
CATEGORIES = {
    "core_structures", "fasteners_bindings", "transmission_media",
    "reactants", "control_agents", "sustenance_sources",
}
FORMS = {"raw", "processed", "refined", "finished"}
ECONOMIC_ROLES = {
    "raw_material", "component", "consumable", "equipment", "tool",
    "ammunition", "catalyst", "trade_good",
}
CROSS_TIER_ROLES = {"none", "limited", "persistent"}
EXTERNAL_RELATION_TYPES = {
    "enemy_drop", "shop", "starter", "world_spawn", "salvage",
    "consumption", "equipment_use", "tool_use", "trade", "system_use",
}
EXTERNAL_SOURCE_TYPES = {"enemy_drop", "shop", "starter", "world_spawn", "salvage", "trade"}
EXTERNAL_USE_TYPES = {"equipment_use", "tool_use", "trade", "system_use"}


class ContentError(ValueError):
    pass


def load_batches(input_dir: Path, schema_path: Optional[Path]) -> List[Tuple[Path, Dict[str, Any]]]:
    if not input_dir.exists():
        raise FileNotFoundError(input_dir)

    schema = None
    if schema_path:
        if jsonschema is None:
            raise ContentError(
                "jsonschema is required when --schema is supplied; install it with "
                "'py -3 -m pip install jsonschema'"
            )
        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.Draft7Validator.check_schema(schema)

    files = sorted(p for p in input_dir.rglob("*.json") if p.resolve() != (schema_path.resolve() if schema_path else None))
    if not files:
        raise ContentError(f"No JSON worker batches found under {input_dir}")

    batches = []
    for path in files:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if schema is not None:
            jsonschema.validate(data, schema)

        semantic_validate_batch(data, path)
        batches.append((path.relative_to(input_dir), data))

    return batches


def _require_key(value: Any, field: str, path: Path) -> str:
    if not isinstance(value, str) or not KEY_RE.fullmatch(value):
        raise ContentError(f"{path}: {field} must be lowercase snake_case key")
    return value


def _reject_extras(record: Dict[str, Any], allowed: Set[str], entity: str, path: Path) -> None:
    extras = set(record) - allowed
    if extras:
        raise ContentError(f"{path}: {entity} has unsupported keys: {sorted(extras)}")


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
        _reject_extras(
            item,
            {
                "slot_id", "key", "display_name", "description", "category", "form",
                "economic_role", "purpose", "region_keys", "tags", "cross_tier_role",
                "rarity_role", "external_sources", "external_sinks", "external_uses",
                "notes",
            },
            "item",
            path,
        )
        for field in (
            "slot_id", "key", "display_name", "description", "category", "form",
            "economic_role", "purpose", "region_keys", "tags", "cross_tier_role",
            "rarity_role", "external_sources", "external_sinks", "external_uses",
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
        if item["category"] not in CATEGORIES or item["form"] not in FORMS:
            raise ContentError(f"{path}: item has invalid category or form")
        if item["economic_role"] not in ECONOMIC_ROLES:
            raise ContentError(f"{path}: item has invalid economic_role")
        if item["cross_tier_role"] not in CROSS_TIER_ROLES:
            raise ContentError(f"{path}: item has invalid cross_tier_role")
        if not isinstance(item["tags"], list) or len(item["tags"]) != len(set(item["tags"])):
            raise ContentError(f"{path}: item.tags must be a unique array")
        for tag in item["tags"]:
            _require_key(tag, "item.tags", path)
        for relation_group in ("external_sources", "external_sinks", "external_uses"):
            if not isinstance(item[relation_group], list):
                raise ContentError(f"{path}: item.{relation_group} must be an array")
            for relation in item[relation_group]:
                if not isinstance(relation, dict):
                    raise ContentError(f"{path}: item.{relation_group} entries must be objects")
                _reject_extras(relation, {"relation_type", "detail"}, "external_relation", path)
                allowed_types = (
                    EXTERNAL_SOURCE_TYPES if relation_group == "external_sources"
                    else {"consumption"} if relation_group == "external_sinks"
                    else EXTERNAL_USE_TYPES
                )
                if relation.get("relation_type") not in allowed_types:
                    raise ContentError(
                        f"{path}: invalid {relation_group} relation_type "
                        f"{relation.get('relation_type')!r}"
                    )
                if not isinstance(relation.get("detail"), str) or not relation["detail"].strip():
                    raise ContentError(f"{path}: external relation detail must be non-empty")

    for action in batch["gathering_actions"]:
        _reject_extras(
            action,
            {
                "slot_id", "key", "display_name", "description", "skill_key",
                "level_band", "required_level", "purpose", "region_keys", "outputs",
                "tool_tags", "tool_item_keys", "notes",
            },
            "gathering_action",
            path,
        )
        for field in (
            "slot_id", "key", "display_name", "skill_key", "level_band",
            "required_level", "purpose", "region_keys", "outputs", "tool_tags",
            "tool_item_keys",
        ):
            if field not in action:
                raise ContentError(f"{path}: gathering action missing {field}")
        _require_key(action["slot_id"], "gathering_action.slot_id", path)
        _require_key(action["key"], "gathering_action.key", path)
        if action["skill_key"] not in SKILLS:
            raise ContentError(f"{path}: invalid gathering action skill")
        if not isinstance(action["level_band"], int) or action["level_band"] < 1:
            raise ContentError(f"{path}: action level_band must be positive integer")
        if not isinstance(action["required_level"], int) or action["required_level"] < 1:
            raise ContentError(f"{path}: action required_level must be positive integer")
        if not isinstance(action["region_keys"], list) or not action["region_keys"]:
            raise ContentError(f"{path}: gathering action region_keys must be non-empty")
        if any(r not in REGIONS for r in action["region_keys"]):
            raise ContentError(f"{path}: gathering action has invalid region")
        if not isinstance(action["tool_item_keys"], list):
            raise ContentError(f"{path}: gathering action tool_item_keys must be an array")
        if len(action["tool_item_keys"]) != len(set(action["tool_item_keys"])):
            raise ContentError(f"{path}: gathering action tool_item_keys must be unique")
        if not isinstance(action["tool_tags"], list):
            raise ContentError(f"{path}: gathering action tool_tags must be an array")
        if len(action["tool_tags"]) != len(set(action["tool_tags"])):
            raise ContentError(f"{path}: gathering action tool_tags must be unique")
        for tool_item_key in action["tool_item_keys"]:
            _require_key(tool_item_key, "gathering_action.tool_item_keys", path)
        for tool_tag in action["tool_tags"]:
            _require_key(tool_tag, "gathering_action.tool_tags", path)
        if not isinstance(action["outputs"], list) or not action["outputs"]:
            raise ContentError(f"{path}: gathering action must have outputs")
        for out in action["outputs"]:
            _reject_extras(
                out,
                {"item_key", "quantity", "mode", "rarity_role", "condition_tag", "rng_rationale"},
                "gathering_output",
                path,
            )
            for field in ("item_key", "quantity", "mode", "rarity_role", "rng_rationale"):
                if field not in out:
                    raise ContentError(f"{path}: gathering output missing {field}")
            _require_key(out["item_key"], "gathering_output.item_key", path)
            if out["mode"] not in {"guaranteed", "weighted", "conditional"}:
                raise ContentError(f"{path}: invalid gathering output mode")
            if out["rarity_role"] not in RARITIES:
                raise ContentError(f"{path}: invalid gathering output rarity")
            if not isinstance(out["quantity"], int) or out["quantity"] < 1:
                raise ContentError(f"{path}: gathering output quantity must be positive integer")
            if out["mode"] == "guaranteed" and out["rng_rationale"] is not None:
                raise ContentError(f"{path}: guaranteed output may not carry rng_rationale")
            if out["mode"] != "guaranteed" and not out["rng_rationale"]:
                raise ContentError(f"{path}: random/conditional output requires rng_rationale")
            if out["mode"] == "conditional" and not out.get("condition_tag"):
                raise ContentError(f"{path}: conditional output requires condition_tag")

        output_item_keys = [out["item_key"] for out in action["outputs"]]
        if len(output_item_keys) != len(set(output_item_keys)):
            raise ContentError(f"{path}: duplicate item reference in action {action['key']} outputs")

        weighted_count = sum(1 for out in action["outputs"] if out["mode"] == "weighted")
        if weighted_count == 1:
            raise ContentError(f"{path}: weighted output pools require at least two alternatives")

    for node in batch["gathering_nodes"]:
        _reject_extras(
            node,
            {
                "slot_id", "key", "display_name", "description", "action_key",
                "region_key", "world_context", "interaction_verb", "depletable",
                "respawnable", "stateful", "notes",
            },
            "gathering_node",
            path,
        )
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
        for flag in ("depletable", "respawnable", "stateful"):
            if not isinstance(node[flag], bool):
                raise ContentError(f"{path}: gathering node {flag} must be boolean")

    for recipe in batch["recipes"]:
        _reject_extras(
            recipe,
            {
                "slot_id", "key", "display_name", "description", "skill_key",
                "level_band", "required_level", "purpose", "region_keys", "inputs",
                "outputs", "station_tag", "cross_skill_links", "notes",
            },
            "recipe",
            path,
        )
        for field in (
            "slot_id", "key", "display_name", "skill_key", "level_band",
            "required_level", "purpose", "region_keys", "inputs", "outputs",
            "cross_skill_links",
        ):
            if field not in recipe:
                raise ContentError(f"{path}: recipe missing {field}")
        _require_key(recipe["slot_id"], "recipe.slot_id", path)
        _require_key(recipe["key"], "recipe.key", path)
        if recipe["skill_key"] not in SKILLS:
            raise ContentError(f"{path}: invalid recipe skill")
        if not isinstance(recipe["level_band"], int) or recipe["level_band"] < 1:
            raise ContentError(f"{path}: recipe level_band must be positive integer")
        if not isinstance(recipe["required_level"], int) or recipe["required_level"] < 1:
            raise ContentError(f"{path}: recipe required_level must be positive integer")
        if not isinstance(recipe["region_keys"], list) or not recipe["region_keys"]:
            raise ContentError(f"{path}: recipe region_keys must be non-empty")
        if any(r not in REGIONS for r in recipe["region_keys"]):
            raise ContentError(f"{path}: recipe has invalid region")
        if any(s not in SKILLS for s in recipe["cross_skill_links"]):
            raise ContentError(f"{path}: recipe has invalid cross_skill_links")
        if not isinstance(recipe["inputs"], list) or not recipe["inputs"]:
            raise ContentError(f"{path}: recipe must have inputs")
        if not isinstance(recipe["outputs"], list) or not recipe["outputs"]:
            raise ContentError(f"{path}: recipe must have outputs")
        for io_group in ("inputs", "outputs"):
            io_item_keys = [io.get("item_key") for io in recipe[io_group]]
            if len(io_item_keys) != len(set(io_item_keys)):
                raise ContentError(
                    f"{path}: duplicate item reference in recipe {recipe['key']} {io_group}"
                )
            for io in recipe[io_group]:
                _reject_extras(io, {"item_key", "quantity"}, "recipe_io", path)
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
    item_roles = {r["key"]: r["economic_role"] for r in data["items"]}
    actions = {r["key"] for r in data["gathering_actions"]}

    errors = []

    for action in data["gathering_actions"]:
        for out in action["outputs"]:
            if out["item_key"] not in items:
                errors.append(f"Action {action['key']} references missing item {out['item_key']}")
        for tool_item_key in action["tool_item_keys"]:
            if tool_item_key not in items:
                errors.append(f"Action {action['key']} references missing tool item {tool_item_key}")
            elif item_roles[tool_item_key] != "tool":
                errors.append(
                    f"Action {action['key']} tool {tool_item_key} is not economic_role=tool"
                )

    for node in data["gathering_nodes"]:
        if node["action_key"] not in actions:
            errors.append(f"Node {node['key']} references missing action {node['action_key']}")
        else:
            action = next(a for a in data["gathering_actions"] if a["key"] == node["action_key"])
            if node["region_key"] not in action["region_keys"]:
                errors.append(
                    f"Node {node['key']} region {node['region_key']} is not declared by "
                    f"action {node['action_key']}"
                )

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

        CREATE TABLE economy_skill_scope (
            skill_key TEXT PRIMARY KEY REFERENCES skills(skill_key),
            skill_kind TEXT NOT NULL CHECK(skill_kind IN ('gathering', 'crafting')),
            target_scope TEXT NOT NULL CHECK(target_scope IN ('v1_core', 'economy_extension')),
            coverage_status TEXT NOT NULL CHECK(coverage_status IN ('covered', 'uncovered'))
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
            required_level INTEGER NOT NULL,
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

        CREATE TABLE gathering_action_tool_items (
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            item_key TEXT NOT NULL REFERENCES items(item_key),
            PRIMARY KEY (action_key, item_key)
        );

        CREATE TABLE gathering_action_outputs (
            action_key TEXT NOT NULL REFERENCES gathering_actions(action_key),
            item_key TEXT NOT NULL REFERENCES items(item_key),
            quantity INTEGER NOT NULL,
            mode TEXT NOT NULL,
            rarity_role TEXT NOT NULL,
            condition_tag TEXT,
            rng_rationale TEXT,
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
            required_level INTEGER NOT NULL,
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

        CREATE TABLE item_uses (
            item_key TEXT NOT NULL REFERENCES items(item_key),
            use_type TEXT NOT NULL,
            use_key TEXT NOT NULL,
            detail TEXT,
            level_band INTEGER,
            skill_key TEXT REFERENCES skills(skill_key),
            PRIMARY KEY (item_key, use_type, use_key)
        );

        CREATE TABLE item_metrics (
            item_key TEXT PRIMARY KEY REFERENCES items(item_key),
            source_count INTEGER NOT NULL,
            sink_count INTEGER NOT NULL,
            use_count INTEGER NOT NULL,
            source_type_count INTEGER NOT NULL,
            sink_type_count INTEGER NOT NULL,
            skills_connected INTEGER NOT NULL,
            regions_connected INTEGER NOT NULL,
            earliest_source_band INTEGER,
            latest_sink_band INTEGER,
            progression_band_span INTEGER,
            latest_source_band INTEGER,
            latest_use_band INTEGER,
            relevance_band_span INTEGER,
            open_ended_demand INTEGER NOT NULL,
            dependency_depth INTEGER,
            cross_tier_reuse_count INTEGER NOT NULL
        );

        CREATE TABLE skill_metrics (
            skill_key TEXT PRIMARY KEY REFERENCES skills(skill_key),
            gathering_action_count INTEGER NOT NULL,
            recipe_count INTEGER NOT NULL,
            distinct_item_count INTEGER NOT NULL,
            covered_band_count INTEGER NOT NULL,
            coverage_status TEXT NOT NULL CHECK(coverage_status IN ('covered', 'uncovered'))
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
        CREATE INDEX idx_uses_item ON item_uses(item_key);
        CREATE INDEX idx_actions_skill_band ON gathering_actions(skill_key, level_band);
        CREATE INDEX idx_actions_skill_level ON gathering_actions(skill_key, required_level);
        CREATE INDEX idx_recipes_skill_band ON recipes(skill_key, level_band);
        CREATE INDEX idx_recipes_skill_level ON recipes(skill_key, required_level);
        CREATE INDEX idx_nodes_action ON gathering_nodes(action_key);

        CREATE VIEW v_item_origins AS
        SELECT gao.item_key,
               'world_node' AS origin_type,
               gn.node_key AS origin_key,
               gn.display_name AS origin_name,
               ga.action_key,
               ga.skill_key,
               gn.region_key,
               ga.required_level
        FROM gathering_action_outputs gao
        JOIN gathering_actions ga ON ga.action_key = gao.action_key
        JOIN gathering_nodes gn ON gn.action_key = ga.action_key
        UNION ALL
        SELECT ro.item_key,
               'recipe' AS origin_type,
               r.recipe_key AS origin_key,
               r.display_name AS origin_name,
               NULL AS action_key,
               r.skill_key,
               rr.region_key,
               r.required_level
        FROM recipe_outputs ro
        JOIN recipes r ON r.recipe_key = ro.recipe_key
        JOIN recipe_regions rr ON rr.recipe_key = r.recipe_key
        UNION ALL
        SELECT s.item_key,
               s.source_type AS origin_type,
               s.source_key AS origin_key,
               COALESCE(s.detail, s.source_key) AS origin_name,
               NULL AS action_key,
               s.skill_key,
               NULL AS region_key,
               NULL AS required_level
        FROM item_sources s
        WHERE s.source_type NOT IN ('gathering', 'recipe');

        CREATE VIEW v_item_transformations AS
        SELECT ri.item_key AS input_item_key,
               r.recipe_key,
               r.display_name AS recipe_name,
               r.skill_key,
               r.required_level,
               ri.quantity AS input_quantity,
               ro.item_key AS output_item_key,
               ro.quantity AS output_quantity
        FROM recipe_inputs ri
        JOIN recipes r ON r.recipe_key = ri.recipe_key
        JOIN recipe_outputs ro ON ro.recipe_key = r.recipe_key;

        CREATE VIEW v_level_unlocks AS
        SELECT required_level,
               skill_key,
               'gathering_action' AS unlock_type,
               action_key AS unlock_key,
               display_name,
               level_band
        FROM gathering_actions
        UNION ALL
        SELECT required_level,
               skill_key,
               'recipe' AS unlock_type,
               recipe_key AS unlock_key,
               display_name,
               level_band
        FROM recipes;

        CREATE VIEW v_activity_rates AS
        SELECT 'gathering' AS activity_type,
               ga.action_key AS activity_key,
               ga.display_name,
               ga.skill_key,
               ga.required_level,
               ga.target_xp_per_hour,
               gao.item_key AS output_item_key,
               gao.mode AS output_mode,
               gao.output_probability,
               gao.expected_quantity_per_hour
        FROM gathering_actions ga
        JOIN gathering_action_outputs gao ON gao.action_key = ga.action_key
        UNION ALL
        SELECT 'crafting' AS activity_type,
               r.recipe_key AS activity_key,
               r.display_name,
               r.skill_key,
               r.required_level,
               r.target_xp_per_hour,
               ro.item_key AS output_item_key,
               'guaranteed' AS output_mode,
               1.0 AS output_probability,
               ROUND(r.attempts_per_hour * ro.quantity, 6) AS expected_quantity_per_hour
        FROM recipes r
        JOIN recipe_outputs ro ON ro.recipe_key = r.recipe_key;

        CREATE VIEW v_item_connections AS
        SELECT i.item_key,
               i.display_name,
               (SELECT GROUP_CONCAT(skill_key, ',') FROM (
                    SELECT DISTINCT skill_key
                    FROM (
                        SELECT skill_key FROM item_sources
                        WHERE item_key = i.item_key AND skill_key IS NOT NULL
                        UNION
                        SELECT skill_key FROM item_sinks
                        WHERE item_key = i.item_key AND skill_key IS NOT NULL
                        UNION
                        SELECT skill_key FROM item_uses
                        WHERE item_key = i.item_key AND skill_key IS NOT NULL
                    ) ORDER BY skill_key
                )) AS skills,
               (SELECT GROUP_CONCAT(region_key, ',') FROM (
                    SELECT DISTINCT region_key
                    FROM v_item_origins
                    WHERE item_key = i.item_key AND region_key IS NOT NULL
                    ORDER BY region_key
                )) AS source_regions,
               m.source_count,
               m.sink_count,
               m.use_count,
               m.progression_band_span,
               m.relevance_band_span,
               m.open_ended_demand,
               m.cross_tier_reuse_count
        FROM items i
        JOIN item_metrics m ON m.item_key = i.item_key;

        CREATE VIEW v_item_health AS
        SELECT i.item_key,
               i.display_name,
               i.economic_role,
               m.source_count,
               m.sink_count,
               m.use_count,
               CASE WHEN m.source_count = 0 THEN 1 ELSE 0 END AS lacks_source,
               CASE WHEN m.sink_count = 0 THEN 1 ELSE 0 END AS lacks_sink,
               m.earliest_source_band,
               m.latest_sink_band,
               m.progression_band_span,
               m.latest_source_band,
               m.latest_use_band,
               m.relevance_band_span,
               m.open_ended_demand,
               m.dependency_depth
        FROM items i
        JOIN item_metrics m ON m.item_key = i.item_key;

        CREATE VIEW v_item_relevance AS
        SELECT i.item_key,
               i.display_name,
               m.earliest_source_band,
               m.latest_source_band,
               m.latest_sink_band,
               m.latest_use_band,
               m.progression_band_span AS consuming_band_span,
               m.relevance_band_span,
               m.open_ended_demand,
               m.cross_tier_reuse_count
        FROM items i
        JOIN item_metrics m ON m.item_key = i.item_key;

        CREATE VIEW v_tool_progression AS
        SELECT ti.item_key AS tool_item_key,
               ti.display_name AS tool_name,
               ga.action_key,
               ga.display_name AS action_name,
               ga.skill_key,
               ga.required_level
        FROM gathering_action_tool_items gat
        JOIN items ti ON ti.item_key = gat.item_key
        JOIN gathering_actions ga ON ga.action_key = gat.action_key;
        """
    )


def seed_reference_tables(conn: sqlite3.Connection) -> None:
    conn.executemany("INSERT INTO regions(region_key) VALUES (?)", [(r,) for r in REGIONS])
    conn.executemany("INSERT INTO skills(skill_key) VALUES (?)", [(s,) for s in SKILLS])
    conn.executemany(
        "INSERT INTO economy_skill_scope VALUES (?, ?, ?, 'uncovered')",
        [
            (
                skill,
                "gathering" if skill in GATHERING_SKILLS else "crafting",
                "v1_core" if skill in V1_CORE_SKILLS else "economy_extension",
            )
            for skill in SKILLS
        ],
    )


def insert_progression(conn: sqlite3.Connection, cfg: Optional[Dict[str, Any]]) -> None:
    if cfg is None:
        return

    conn.execute("INSERT INTO metadata(key, value) VALUES (?, ?)", ("balance_status", str(cfg["status"])))
    conn.execute(
        "INSERT INTO metadata(key, value) VALUES (?, ?)",
        ("balance_config_json", json.dumps(cfg, sort_keys=True, separators=(",", ":"))),
    )

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
                action_key, slot_id, display_name, description, skill_key, level_band,
                required_level, purpose,
                action_seconds, success_chance, target_xp_per_hour, xp_per_action,
                attempts_per_hour, notes, source_batch, source_file
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                action["key"], action["slot_id"], action["display_name"], action.get("description"),
                action["skill_key"], action["level_band"], action["required_level"],
                action["purpose"],
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
        for tool_item_key in sorted(set(action["tool_item_keys"])):
            conn.execute(
                "INSERT INTO gathering_action_tool_items VALUES (?, ?)",
                (action["key"], tool_item_key),
            )

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
                        * math["yield_multiplier"]
                    )

            conn.execute(
                """
                INSERT INTO gathering_action_outputs(
                    action_key, item_key, quantity, mode, rarity_role, condition_tag,
                    rng_rationale, relative_weight, output_probability,
                    expected_quantity_per_hour
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    action["key"], out["item_key"], out["quantity"], out["mode"],
                    out["rarity_role"], out.get("condition_tag"), out["rng_rationale"],
                    relative_weight, probability, expected_per_hour,
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
                recipe_key, slot_id, display_name, description, skill_key, level_band,
                required_level, purpose,
                station_tag, action_seconds, target_xp_per_hour, xp_per_action,
                attempts_per_hour, notes, source_batch, source_file
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recipe["key"], recipe["slot_id"], recipe["display_name"], recipe.get("description"),
                recipe["skill_key"], recipe["level_band"], recipe["required_level"],
                recipe["purpose"],
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

    for action_key, item_key, level_band, skill_key in conn.execute(
        """
        SELECT ga.action_key, gati.item_key, ga.level_band, ga.skill_key
        FROM gathering_action_tool_items gati
        JOIN gathering_actions ga ON ga.action_key = gati.action_key
        """
    ):
        conn.execute(
            """
            INSERT INTO item_uses(item_key, use_type, use_key, detail, level_band, skill_key)
            VALUES (?, 'tool_requirement', ?, 'Compatible gathering tool', ?, ?)
            """,
            (item_key, action_key, level_band, skill_key),
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
        for i, rel in enumerate(item["external_sinks"], 1):
            relation_key = f"consumption:{i}:{item_key}"
            conn.execute(
                """
                INSERT INTO item_sinks(item_key, sink_type, sink_key, detail, level_band, skill_key)
                VALUES (?, 'consumption', ?, ?, NULL, NULL)
                """,
                (item_key, relation_key, rel["detail"]),
            )
        for i, rel in enumerate(item["external_uses"], 1):
            relation_key = f"{rel['relation_type']}:{i}:{item_key}"
            conn.execute(
                """
                INSERT INTO item_uses(item_key, use_type, use_key, detail, level_band, skill_key)
                VALUES (?, ?, ?, ?, NULL, NULL)
                """,
                (item_key, rel["relation_type"], relation_key, rel["detail"]),
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
    successors: Dict[str, Set[str]] = defaultdict(set)
    for input_item, output_item in conn.execute(
        "SELECT input_item_key, output_item_key FROM v_item_transformations"
    ):
        if input_item != output_item:
            successors[input_item].add(output_item)

    def reachable_items(start: str) -> Set[str]:
        reached = {start}
        pending = [start]
        while pending:
            current = pending.pop()
            for nxt in successors[current]:
                if nxt not in reached:
                    reached.add(nxt)
                    pending.append(nxt)
        return reached

    for item_key in sorted(item_map):
        source_count = conn.execute(
            "SELECT COUNT(*) FROM item_sources WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        sink_count = conn.execute(
            "SELECT COUNT(*) FROM item_sinks WHERE item_key = ?", (item_key,)
        ).fetchone()[0]
        use_count = conn.execute(
            "SELECT COUNT(*) FROM item_uses WHERE item_key = ?", (item_key,)
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
                UNION
                SELECT skill_key FROM item_uses WHERE item_key = ? AND skill_key IS NOT NULL
            )
            """,
            (item_key, item_key, item_key),
        ).fetchone()[0]
        regions_connected = conn.execute(
            """
            SELECT COUNT(DISTINCT region_key)
            FROM v_item_origins
            WHERE item_key = ? AND region_key IS NOT NULL
            """,
            (item_key,),
        ).fetchone()[0]
        earliest_source_band = conn.execute(
            """
            SELECT MIN(CASE
                           WHEN source_type IN ('starter', 'shop') THEN 0
                           ELSE level_band
                       END)
            FROM item_sources
            WHERE item_key = ?
            """,
            (item_key,),
        ).fetchone()[0]
        latest_source_band = conn.execute(
            "SELECT MAX(level_band) FROM item_sources WHERE item_key = ?",
            (item_key,),
        ).fetchone()[0]
        latest_use_band = conn.execute(
            "SELECT MAX(level_band) FROM item_uses WHERE item_key = ?",
            (item_key,),
        ).fetchone()[0]
        open_ended_demand = conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT use_key FROM item_uses
                WHERE item_key = ? AND level_band IS NULL
                UNION ALL
                SELECT sink_key FROM item_sinks
                WHERE item_key = ? AND sink_type = 'consumption' AND level_band IS NULL
            )
            """,
            (item_key, item_key),
        ).fetchone()[0]
        reachable = sorted(reachable_items(item_key))
        placeholders = ",".join("?" for _ in reachable)
        latest_sink_band = conn.execute(
            f"SELECT MAX(level_band) FROM item_sinks WHERE item_key IN ({placeholders})",
            reachable,
        ).fetchone()[0]

        span = None
        relevance_span = None
        cross_tier_reuse = 0
        known_end_bands = [
            band for band in (latest_source_band, latest_sink_band, latest_use_band)
            if band is not None
        ]
        if earliest_source_band is not None and known_end_bands:
            relevance_span = max(known_end_bands) - int(earliest_source_band)
        if earliest_source_band is not None and latest_sink_band is not None:
            span = int(latest_sink_band) - int(earliest_source_band)
            cross_tier_reuse = conn.execute(
                f"""
                SELECT COUNT(*)
                FROM item_sinks
                WHERE item_key IN ({placeholders})
                  AND level_band IS NOT NULL
                  AND level_band >= ?
                """,
                (*reachable, int(earliest_source_band) + 2),
            ).fetchone()[0]

        conn.execute(
            """
            INSERT INTO item_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_key, source_count, sink_count, use_count,
                source_type_count, sink_type_count,
                skills_connected, regions_connected, earliest_source_band, latest_sink_band,
                span, latest_source_band, latest_use_band, relevance_span,
                int(open_ended_demand > 0), depth.get(item_key, 0), cross_tier_reuse,
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
        if sink_count == 0 and item["economic_role"] in {"consumable", "ammunition"}:
            add_finding(
                conn, "error", "unconsumed_terminal", "item", item_key,
                f"{item['economic_role']} has no modeled removal/consumption pathway."
            )
        if sink_count == 0 and use_count == 0 and item["economic_role"] in {"equipment", "tool"}:
            add_finding(
                conn, "warning", "unused_terminal", "item", item_key,
                f"{item['economic_role']} has no modeled use or consuming sink."
            )

        reachable_consumption_count = conn.execute(
            f"SELECT COUNT(*) FROM item_sinks WHERE item_key IN ({placeholders})",
            reachable,
        ).fetchone()[0]
        if (
            sink_count <= 1
            and reachable_consumption_count <= 1
            and item["economic_role"] not in TERMINAL_ROLES
            and item["cross_tier_role"] == "persistent"
        ):
            add_finding(
                conn, "warning", "weak_sink", "item", item_key,
                "Persistent non-terminal item has at most one consuming sink across its reachable recipe graph."
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

        coverage_status = "covered" if gather_count + recipe_count > 0 else "uncovered"
        conn.execute(
            "INSERT INTO skill_metrics VALUES (?, ?, ?, ?, ?, ?)",
            (
                skill, gather_count, recipe_count, distinct_item_count,
                covered_band_count, coverage_status,
            ),
        )
        conn.execute(
            "UPDATE economy_skill_scope SET coverage_status = ? WHERE skill_key = ?",
            (coverage_status, skill),
        )
        if coverage_status == "uncovered":
            add_finding(
                conn, "warning", "uncovered_economy_skill", "skill", skill,
                "Included analytical economy skill has no modeled gathering action or recipe."
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

    for action_key in (
        row[0] for row in conn.execute(
            """
            SELECT ga.action_key
            FROM gathering_actions ga
            LEFT JOIN gathering_nodes gn ON gn.action_key = ga.action_key
            GROUP BY ga.action_key
            HAVING COUNT(gn.node_key) = 0
            ORDER BY ga.action_key
            """
        )
    ):
        add_finding(
            conn, "error", "action_without_node", "gathering_action", action_key,
            "Gathering action has no world node."
        )

    for action_key, action_band, earliest_compatible_tool_band in conn.execute(
        """
        SELECT ga.action_key, ga.level_band,
               MIN(CASE
                       WHEN s.source_type IN ('starter', 'shop') THEN 0
                       WHEN s.level_band IS NULL THEN 999
                       ELSE s.level_band
                   END)
        FROM gathering_actions ga
        JOIN gathering_action_tool_items gati ON gati.action_key = ga.action_key
        LEFT JOIN item_sources s ON s.item_key = gati.item_key
        GROUP BY ga.action_key, ga.level_band
        ORDER BY ga.action_key
        """
    ):
        if earliest_compatible_tool_band == 999:
            add_finding(
                conn, "error", "unavailable_tool", "gathering_action", action_key,
                "No compatible tool has a modeled source."
            )
        elif earliest_compatible_tool_band > action_band:
            add_finding(
                conn, "error", "tool_progression_block", "gathering_action", action_key,
                f"Every compatible tool first appears after the action's band {action_band}."
            )

    for recipe_key, item_key, recipe_band, source_band in conn.execute(
        """
        SELECT r.recipe_key, ri.item_key, r.level_band,
               MIN(CASE
                       WHEN s.source_type IN ('starter', 'shop') THEN 0
                       WHEN s.level_band IS NULL THEN 999
                       ELSE s.level_band
                   END)
        FROM recipes r
        JOIN recipe_inputs ri ON ri.recipe_key = r.recipe_key
        LEFT JOIN item_sources s ON s.item_key = ri.item_key
        GROUP BY r.recipe_key, ri.item_key, r.level_band
        ORDER BY r.recipe_key, ri.item_key
        """
    ):
        if source_band == 999:
            add_finding(
                conn, "error", "unavailable_recipe_input", "recipe", recipe_key,
                f"Input {item_key} has no modeled source."
            )
        elif source_band > recipe_band:
            add_finding(
                conn, "error", "recipe_progression_block", "recipe", recipe_key,
                f"Input {item_key} first appears in band {source_band}, after recipe band {recipe_band}."
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
        "item_uses", "economy_skill_scope",
        "validation_findings",
    ):
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    severities = dict(
        conn.execute(
            "SELECT severity, COUNT(*) FROM validation_findings GROUP BY severity"
        ).fetchall()
    )
    missing_sources = conn.execute(
        "SELECT COUNT(*) FROM item_metrics WHERE source_count = 0"
    ).fetchone()[0]
    missing_consuming_sinks = conn.execute(
        "SELECT COUNT(*) FROM item_metrics WHERE sink_count = 0"
    ).fetchone()[0]
    uncovered_skills = conn.execute(
        "SELECT COUNT(*) FROM economy_skill_scope WHERE coverage_status = 'uncovered'"
    ).fetchone()[0]
    random_outputs = conn.execute(
        "SELECT COUNT(*) FROM gathering_action_outputs WHERE mode != 'guaranteed'"
    ).fetchone()[0]
    unresolved_rates = conn.execute(
        "SELECT COUNT(*) FROM gathering_action_outputs WHERE expected_quantity_per_hour IS NULL"
    ).fetchone()[0]

    top_connected = conn.execute(
        """
        SELECT i.item_key, i.display_name, m.source_count, m.sink_count,
               m.use_count, m.skills_connected, m.progression_band_span,
               m.relevance_band_span, m.open_ended_demand
        FROM item_metrics m
        JOIN items i ON i.item_key = m.item_key
        ORDER BY (m.source_count + m.sink_count + m.use_count) DESC, i.item_key
        LIMIT 15
        """
    ).fetchall()

    lines = [
        "# Caelmor Economy Database Audit",
        "",
        "## Row counts",
        "",
        "| Relation | Rows |",
        "|---|---:|",
    ]
    for table, count in counts.items():
        lines.append(f"| `{table}` | {count:,} |")

    lines += [
        "", "## Coverage and graph health", "",
        f"- Included analytical economy skills covered: {len(SKILLS) - uncovered_skills}/{len(SKILLS)}; "
        f"uncovered: {uncovered_skills}.",
        f"- Items without a modeled source: {missing_sources}.",
        f"- Items without a consuming sink: {missing_consuming_sinks} "
        "(reusable equipment/tools may intentionally have none).",
        f"- Non-guaranteed gathering outputs: {random_outputs}; unresolved "
        f"yield rates: {unresolved_rates}.",
        "- Balance status: " + (
            conn.execute("SELECT value FROM metadata WHERE key = 'balance_status'").fetchone() or ("unconfigured",)
        )[0] + ".",
    ]

    lines += [
        "",
        "## Validation findings",
        "",
        "Consuming sinks count recipe-input removal and explicit item `consumption` only. "
        "Trade, equipment/tool use, tool requirements, and other non-consuming "
        "demand are counted separately in `item_uses`.",
        "",
        f"- Errors: {severities.get('error', 0):,}",
        f"- Warnings: {severities.get('warning', 0):,}",
        f"- Informational: {severities.get('info', 0):,}",
        "",
        "## Most connected items",
        "",
        "| Item | Sources | Consuming sinks | Uses/demand | Skills | Consuming band span | Relevance band span | Open-ended demand |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in top_connected:
        lines.append(
            f"| `{row[0]}` | {row[2]} | {row[3]} | {row[4]} | {row[5]} | "
            f"{row[6]} | {row[7]} | {'yes' if row[8] else 'no'} |"
        )

    lines += ["", "## Detailed findings", ""]
    findings = conn.execute(
        """
        SELECT severity, finding_type, entity_type, entity_key, detail
        FROM validation_findings
        ORDER BY CASE severity WHEN 'error' THEN 0 WHEN 'warning' THEN 1 ELSE 2 END,
                 finding_type, entity_key
        """
    ).fetchall()
    if not findings:
        lines.append("No validation findings.")
    else:
        for severity, finding_type, entity_type, entity_key, detail in findings:
            lines.append(
                f"- **{severity.upper()} `{finding_type}`** — {entity_type} "
                f"`{entity_key}`: {detail}"
            )

    lines += [
        "", "## Economy skill scope", "",
        "Phase 1.3 defines seven `v1_core` skills. The seven `economy_extension` skills "
        "come from later Stage 3.1 analytical planning; they are post-v1 economy content, "
        "not automatically authorized v1 runtime scope. All 14 included skills are "
        "validated for coverage; `uncovered` is a warning, not an omitted row.",
        "", "| Skill | Kind | Target | Status | Actions | Recipes | Items | Bands |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]
    for row in conn.execute(
        """
        SELECT s.skill_key, s.skill_kind, s.target_scope, s.coverage_status,
               m.gathering_action_count, m.recipe_count,
               m.distinct_item_count, m.covered_band_count
        FROM economy_skill_scope s
        JOIN skill_metrics m ON m.skill_key = s.skill_key
        ORDER BY s.skill_key
        """
    ):
        lines.append(
            f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | "
            f"{row[4]} | {row[5]} | {row[6]} | {row[7]} |"
        )

    lines += [
        "",
        "## Analytical entry points",
        "",
        "Use `v_item_origins`, `v_item_transformations`, `v_item_connections`, "
        "`v_item_health`, `v_item_relevance`, `v_level_unlocks`, `v_activity_rates`, and "
        "`v_tool_progression` for the primary design questions.",
    ]

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
        bands = band_map(cfg)
        for collection in ("gathering_actions", "recipes"):
            for record in data[collection]:
                if record["level_band"] not in valid_band_ids:
                    raise ContentError(
                        f"{collection} {record['key']} uses level_band {record['level_band']} "
                        "which does not exist in the progression config"
                    )
                band = bands[record["level_band"]]
                if not band["level_min"] <= record["required_level"] <= band["level_max"]:
                    raise ContentError(
                        f"{collection} {record['key']} required_level "
                        f"{record['required_level']} is outside band {record['level_band']} "
                        f"({band['level_min']}..{band['level_max']})"
                    )

    output_db.parent.mkdir(parents=True, exist_ok=True)
    temp_db = output_db.with_suffix(output_db.suffix + ".tmp")
    if temp_db.exists():
        temp_db.unlink()

    conn = connect(temp_db)
    try:
        create_schema(conn)
        seed_reference_tables(conn)
        canonical_content = json.dumps(data, sort_keys=True, separators=(",", ":"))
        conn.executemany(
            "INSERT INTO metadata(key, value) VALUES (?, ?)",
            [
                ("schema_version", "4"),
                ("v1_scope_authority", "Phase 1.3 Feature Set & Scope Boundaries"),
                ("economy_extension_status", "post-v1 analytical planning; not authorized v1 runtime scope"),
                ("interchange_schema_sha256", hashlib.sha256(schema_path.read_bytes()).hexdigest() if schema_path else "none"),
                ("content_sha256", hashlib.sha256(canonical_content.encode("utf-8")).hexdigest()),
                ("progression_config_sha256", hashlib.sha256(progression_config.read_bytes()).hexdigest() if progression_config else "none"),
            ],
        )
        insert_progression(conn, cfg)
        insert_content(conn, data, cfg)
        build_sources_and_sinks(conn, data)
        calculate_metrics_and_findings(conn, data, cfg)

        fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
        if fk_errors:
            raise ContentError(f"SQLite foreign key check failed: {fk_errors}")
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise ContentError(f"SQLite integrity_check failed: {integrity}")

        conn.commit()
        text = report(conn)
    except Exception:
        conn.rollback()
        conn.close()
        if temp_db.exists():
            temp_db.unlink()
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass

    temp_db.replace(output_db)

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
                "external_uses": [],
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
                "external_uses": [],
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
                "external_sources": [
                    {"relation_type": "starter", "detail": "Self-test starter tool."}
                ],
                "external_sinks": [
                ],
                "external_uses": [
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
                "required_level": 1,
                "purpose": "Core early Mining progression.",
                "region_keys": ["lowmark"],
                "outputs": [
                    {
                        "item_key": "iron_ore",
                        "quantity": 1,
                        "mode": "guaranteed",
                        "rarity_role": "common",
                        "condition_tag": None,
                        "rng_rationale": None
                    }
                ],
                "tool_tags": ["pick"],
                "tool_item_keys": ["iron_knife"],
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
                "required_level": 1,
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
                "required_level": 21,
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
