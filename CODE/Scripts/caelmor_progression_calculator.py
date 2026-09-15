#!/usr/bin/env python3
"""
Deterministic numeric layer for the Caelmor economy dataset.

This module deliberately contains formulas but no authoritative Caelmor balance
constants. Supply a progression config JSON. The same config + semantic content
always produces the same outputs.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


class BalanceConfigError(ValueError):
    pass


def load_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    validate_config(cfg)
    return cfg


def validate_config(cfg: Dict[str, Any]) -> None:
    required = ["status", "max_level", "curve", "bands", "rarity_weights", "skill_profiles"]
    missing = [k for k in required if k not in cfg]
    if missing:
        raise BalanceConfigError(f"Missing config keys: {missing}")

    max_level = cfg["max_level"]
    if not isinstance(max_level, int) or max_level < 2:
        raise BalanceConfigError("max_level must be an integer >= 2")

    curve = cfg["curve"]
    if curve.get("kind") not in {"power", "osrs_shape"}:
        raise BalanceConfigError("curve.kind must be 'power' or 'osrs_shape'")

    if curve["kind"] == "power":
        for key in ("total_xp_at_max", "exponent"):
            if not isinstance(curve.get(key), (int, float)) or curve[key] <= 0:
                raise BalanceConfigError(f"curve.{key} must be > 0")

    bands = cfg["bands"]
    if not isinstance(bands, list) or not bands:
        raise BalanceConfigError("bands must be a non-empty list")

    seen = set()
    expected_start = 1
    for band in bands:
        band_id = band.get("id")
        if not isinstance(band_id, int) or band_id < 1 or band_id in seen:
            raise BalanceConfigError("band ids must be unique positive integers")
        seen.add(band_id)

        lo = band.get("level_min")
        hi = band.get("level_max")
        if not isinstance(lo, int) or not isinstance(hi, int) or lo > hi:
            raise BalanceConfigError(f"Invalid level range for band {band_id}")
        if lo != expected_start:
            raise BalanceConfigError("bands must be contiguous and start at level 1")
        expected_start = hi + 1

        for key in (
            "target_xp_per_hour",
            "gather_action_seconds",
            "craft_action_seconds",
            "gather_success_chance",
            "weighted_bonus_roll_chance",
        ):
            if not isinstance(band.get(key), (int, float)):
                raise BalanceConfigError(f"band {band_id} missing numeric {key}")

        if not 0 < band["gather_success_chance"] <= 1:
            raise BalanceConfigError("gather_success_chance must be in (0, 1]")
        if not 0 <= band["weighted_bonus_roll_chance"] <= 1:
            raise BalanceConfigError("weighted_bonus_roll_chance must be in [0, 1]")

    if expected_start - 1 != max_level:
        raise BalanceConfigError("bands must cover exactly levels 1..max_level")

    rarity = cfg["rarity_weights"]
    for role in ("common", "uncommon", "rare", "special"):
        if not isinstance(rarity.get(role), (int, float)) or rarity[role] <= 0:
            raise BalanceConfigError(f"rarity_weights.{role} must be > 0")

    if not isinstance(cfg["skill_profiles"], dict):
        raise BalanceConfigError("skill_profiles must be an object")


def xp_table(cfg: Dict[str, Any]) -> List[Dict[str, Optional[int]]]:
    max_level = cfg["max_level"]
    curve = cfg["curve"]

    if curve["kind"] == "osrs_shape":
        totals = _osrs_shape(max_level)
        target = curve.get("total_xp_at_max")
        if target is not None:
            if not isinstance(target, (int, float)) or target <= 0:
                raise BalanceConfigError("curve.total_xp_at_max must be > 0 when supplied")
            raw_max = totals[max_level]
            scale = target / raw_max if raw_max else 1.0
            totals = {level: int(round(xp * scale)) for level, xp in totals.items()}
    else:
        target = float(curve["total_xp_at_max"])
        exponent = float(curve["exponent"])
        totals = {}
        denom = max_level - 1
        for level in range(1, max_level + 1):
            t = (level - 1) / denom
            totals[level] = int(round(target * (t ** exponent)))

    rows = []
    for level in range(1, max_level + 1):
        total = totals[level]
        next_total = totals.get(level + 1)
        rows.append(
            {
                "level": level,
                "total_xp": total,
                "xp_to_next": None if next_total is None else next_total - total,
            }
        )
    return rows


def _osrs_shape(max_level: int) -> Dict[int, int]:
    total = 0
    totals = {1: 0}
    for i in range(1, max_level):
        total = math.floor(total + i + 300 * math.pow(2, i / 7))
        totals[i + 1] = math.floor(total / 4)
    return totals


def band_map(cfg: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    return {int(b["id"]): b for b in cfg["bands"]}


def skill_profile(cfg: Dict[str, Any], skill_key: str) -> Dict[str, float]:
    raw = cfg["skill_profiles"].get(skill_key, {})
    return {
        "xp_rate_multiplier": float(raw.get("xp_rate_multiplier", 1.0)),
        "action_time_multiplier": float(raw.get("action_time_multiplier", 1.0)),
        "yield_multiplier": float(raw.get("yield_multiplier", 1.0)),
    }


def derive_action_math(
    cfg: Dict[str, Any],
    skill_key: str,
    level_band: int,
    activity_kind: str,
) -> Dict[str, float]:
    bands = band_map(cfg)
    if level_band not in bands:
        raise BalanceConfigError(f"Unknown level_band {level_band}")

    band = bands[level_band]
    profile = skill_profile(cfg, skill_key)

    if activity_kind == "gathering":
        seconds = float(band["gather_action_seconds"]) * profile["action_time_multiplier"]
        success = float(band["gather_success_chance"])
        xp_mode = cfg.get("gather_xp_award_mode", "success")
    elif activity_kind == "crafting":
        seconds = float(band["craft_action_seconds"]) * profile["action_time_multiplier"]
        success = 1.0
        xp_mode = cfg.get("craft_xp_award_mode", "attempt")
    else:
        raise BalanceConfigError("activity_kind must be 'gathering' or 'crafting'")

    if seconds <= 0:
        raise BalanceConfigError("derived action duration must be > 0")

    target_xph = float(band["target_xp_per_hour"]) * profile["xp_rate_multiplier"]
    attempts_per_hour = 3600.0 / seconds

    if xp_mode == "success":
        successful_actions_per_hour = attempts_per_hour * success
        if successful_actions_per_hour <= 0:
            raise BalanceConfigError("successful actions/hour must be > 0")
        xp_per_action = target_xph / successful_actions_per_hour
    elif xp_mode == "attempt":
        xp_per_action = target_xph / attempts_per_hour
    else:
        raise BalanceConfigError(f"Unsupported xp award mode: {xp_mode}")

    return {
        "action_seconds": round(seconds, 6),
        "success_chance": round(success, 8),
        "target_xp_per_hour": round(target_xph, 6),
        "attempts_per_hour": round(attempts_per_hour, 6),
        "xp_per_action": round(xp_per_action, 6),
    }


def derive_output_math(
    cfg: Dict[str, Any],
    outputs: List[Dict[str, Any]],
    action_math: Dict[str, float],
) -> List[Dict[str, Any]]:
    rarity_weights = cfg["rarity_weights"]
    weighted = [o for o in outputs if o["mode"] == "weighted"]
    total_weight = sum(float(rarity_weights[o["rarity_role"]]) for o in weighted)

    bonus_roll_chance = None
    # output math is called after action math; callers should add the band-specific
    # bonus roll chance if they need exact weighted probabilities.
    result = []
    for o in outputs:
        entry = dict(o)
        if o["mode"] == "guaranteed":
            output_probability = action_math["success_chance"]
        elif o["mode"] == "weighted":
            entry["relative_weight"] = float(rarity_weights[o["rarity_role"]])
            entry["weighted_pool_total"] = total_weight
            output_probability = None
        else:
            output_probability = None

        entry["output_probability"] = output_probability
        if output_probability is not None:
            entry["expected_quantity_per_hour"] = round(
                action_math["attempts_per_hour"]
                * output_probability
                * int(o["quantity"]),
                6,
            )
        else:
            entry["expected_quantity_per_hour"] = None
        result.append(entry)
    return result


def weighted_probability(
    cfg: Dict[str, Any],
    level_band: int,
    rarity_role: str,
    weighted_outputs: Iterable[Dict[str, Any]],
) -> float:
    bands = band_map(cfg)
    band = bands[level_band]
    bonus_roll = float(band["weighted_bonus_roll_chance"])
    rarity_weights = cfg["rarity_weights"]
    pool = list(weighted_outputs)
    total = sum(float(rarity_weights[o["rarity_role"]]) for o in pool)
    if total <= 0:
        return 0.0
    return bonus_roll * float(rarity_weights[rarity_role]) / total


def write_template(path: Path) -> None:
    template = {
        "status": "PROVISIONAL_REPLACE_WITH_CREATIVE_DIRECTOR_APPROVED_VALUES",
        "max_level": 60,
        "curve": {
            "kind": "power",
            "total_xp_at_max": 1000000,
            "exponent": 2.4
        },
        "gather_xp_award_mode": "success",
        "craft_xp_award_mode": "attempt",
        "bands": [
            {
                "id": 1,
                "level_min": 1,
                "level_max": 10,
                "target_xp_per_hour": 1000,
                "gather_action_seconds": 4.0,
                "craft_action_seconds": 3.0,
                "gather_success_chance": 0.85,
                "weighted_bonus_roll_chance": 0.05
            },
            {
                "id": 2,
                "level_min": 11,
                "level_max": 20,
                "target_xp_per_hour": 1800,
                "gather_action_seconds": 4.5,
                "craft_action_seconds": 3.2,
                "gather_success_chance": 0.88,
                "weighted_bonus_roll_chance": 0.06
            },
            {
                "id": 3,
                "level_min": 21,
                "level_max": 30,
                "target_xp_per_hour": 3000,
                "gather_action_seconds": 5.0,
                "craft_action_seconds": 3.5,
                "gather_success_chance": 0.9,
                "weighted_bonus_roll_chance": 0.07
            },
            {
                "id": 4,
                "level_min": 31,
                "level_max": 40,
                "target_xp_per_hour": 4600,
                "gather_action_seconds": 5.5,
                "craft_action_seconds": 3.8,
                "gather_success_chance": 0.92,
                "weighted_bonus_roll_chance": 0.08
            },
            {
                "id": 5,
                "level_min": 41,
                "level_max": 50,
                "target_xp_per_hour": 6500,
                "gather_action_seconds": 6.0,
                "craft_action_seconds": 4.0,
                "gather_success_chance": 0.94,
                "weighted_bonus_roll_chance": 0.09
            },
            {
                "id": 6,
                "level_min": 51,
                "level_max": 60,
                "target_xp_per_hour": 9000,
                "gather_action_seconds": 6.5,
                "craft_action_seconds": 4.3,
                "gather_success_chance": 0.96,
                "weighted_bonus_roll_chance": 0.1
            }
        ],
        "rarity_weights": {
            "common": 1000,
            "uncommon": 250,
            "rare": 50,
            "special": 10
        },
        "skill_profiles": {}
    }
    path.write_text(json.dumps(template, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_template = sub.add_parser("write-template")
    p_template.add_argument("path", type=Path)

    p_curve = sub.add_parser("curve")
    p_curve.add_argument("config", type=Path)
    p_curve.add_argument("--out", type=Path)

    args = parser.parse_args()

    if args.cmd == "write-template":
        write_template(args.path)
        print(f"Wrote provisional config template: {args.path}")
        return

    cfg = load_config(args.config)
    rows = xp_table(cfg)
    payload = {
        "config_status": cfg["status"],
        "max_level": cfg["max_level"],
        "levels": rows,
    }
    text = json.dumps(payload, indent=2)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote XP curve: {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
