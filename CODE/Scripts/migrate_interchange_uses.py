#!/usr/bin/env python3
"""One-time mechanical migration of pre-split worker item relationships.

Moves non-consuming relations out of ``external_sinks`` into ``external_uses``.
It never touches SQLite and is idempotent. Review the resulting diff before build.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


USE_TYPES = {"equipment_use", "tool_use", "trade", "system_use"}


def migrate(path: Path) -> bool:
    batch = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for item in batch["items"]:
        sinks = item["external_sinks"]
        uses = item.get("external_uses", [])
        retained = []
        for relation in sinks:
            if relation["relation_type"] in USE_TYPES:
                if relation not in uses:
                    uses.append(relation)
                changed = True
            else:
                retained.append(relation)
        if len(retained) != len(sinks):
            item["external_sinks"] = retained
        if "external_uses" not in item:
            item["external_uses"] = uses
            changed = True
    if changed:
        path.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    args = parser.parse_args()
    for path in sorted(args.input_dir.glob("*.json")):
        print(f"{path}: {'migrated' if migrate(path) else 'unchanged'}")


if __name__ == "__main__":
    main()
