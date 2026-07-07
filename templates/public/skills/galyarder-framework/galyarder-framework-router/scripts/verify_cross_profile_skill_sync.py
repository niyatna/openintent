#!/usr/bin/env python3
"""Verify Keiya/default and Galyarder profile skill roots after a selective sync.

This script is intentionally self-contained so future sessions can run it without
reconstructing the audit from memory.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

DEFAULT_KEIYA_ROOT = Path("/home/galyarder/.hermes/skills")
DEFAULT_KEIYA_CONFIG = Path("/home/galyarder/.hermes/config.yaml")
DEFAULT_GALYARDER_ROOT = Path("/home/galyarder/.hermes/profiles/galyarder/skills")
DEFAULT_GALYARDER_CONFIG = Path("/home/galyarder/.hermes/profiles/galyarder/config.yaml")


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _frontmatter(path: Path) -> tuple[dict[str, Any], str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}, None
    end = text.find("\n---", 3)
    if end == -1:
        return {}, "frontmatter closing marker not found"
    raw = text[3:end]
    try:
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            return {}, "frontmatter is not a mapping"
        return data, None
    except Exception as exc:  # noqa: BLE001 - verifier must report exact YAML exception
        return {}, str(exc)


def scan(root: Path, config: Path) -> dict[str, Any]:
    conf = _load_yaml(config)
    disabled = set((conf.get("skills") or {}).get("disabled") or [])
    items: dict[str, dict[str, Any]] = {}
    duplicates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bad_frontmatter: list[dict[str, str]] = []

    for skill_md in root.rglob("SKILL.md"):
        if ".hub" in skill_md.parts or ".archive" in skill_md.parts:
            continue
        rel = skill_md.relative_to(root)
        fm, err = _frontmatter(skill_md)
        if err:
            bad_frontmatter.append({"path": str(rel), "error": err})
        name = fm.get("name") or skill_md.parent.name
        rec = {
            "name": name,
            "rel": str(rel),
            "dir": str(skill_md.parent.relative_to(root)),
            "description": fm.get("description", ""),
            "enabled": name not in disabled,
        }
        if name in items:
            duplicates[name].append(items[name])
            duplicates[name].append(rec)
        items[name] = rec

    folder_slugs = {Path(rec["dir"]).name for rec in items.values()}
    valid_disabled = sorted([d for d in disabled if d in items or d in folder_slugs])
    unmatched_disabled = sorted(disabled - set(valid_disabled))

    lock: dict[str, Any] = {}
    lock_path = root / ".hub" / "lock.json"
    if lock_path.exists():
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8")).get("installed", {})
        except Exception as exc:  # noqa: BLE001
            bad_frontmatter.append({"path": str(lock_path.relative_to(root)), "error": f"lock json: {exc}"})

    return {
        "items": items,
        "duplicates": dict(duplicates),
        "bad_frontmatter": bad_frontmatter,
        "disabled": sorted(disabled),
        "valid_disabled": valid_disabled,
        "unmatched_disabled": unmatched_disabled,
        "lock": lock,
    }


def provenance(inventory: dict[str, Any], name: str) -> str:
    entry = inventory["lock"].get(name) or {}
    identifier = entry.get("identifier", "") or ""
    source = entry.get("source", "") or ""
    if name not in inventory["lock"]:
        return "local/bundled"
    if "anthropics/skills" in identifier:
        return "Anthropic"
    if source == "lobehub" or identifier.startswith("lobehub") or "lobehub" in identifier.lower():
        return "LobeHub"
    if source == "clawhub":
        return "LobeHub/legacy-clawhub"
    if source == "official" or identifier.startswith("official/") or "NousResearch/hermes-agent/optional-skills" in identifier:
        return "Optional"
    return source or "hub-unknown"


def group_by_category(inventory: dict[str, Any], names: set[str]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for name in sorted(names):
        rec = inventory["items"][name]
        parts = Path(rec["dir"]).parts
        category = parts[0] if parts else "(root)"
        grouped[category].append(
            {
                "name": name,
                "provenance": provenance(inventory, name),
                "description": rec["description"],
                "path": rec["dir"],
            }
        )
    return dict(sorted(grouped.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keiya-root", type=Path, default=DEFAULT_KEIYA_ROOT)
    parser.add_argument("--keiya-config", type=Path, default=DEFAULT_KEIYA_CONFIG)
    parser.add_argument("--galyarder-root", type=Path, default=DEFAULT_GALYARDER_ROOT)
    parser.add_argument("--galyarder-config", type=Path, default=DEFAULT_GALYARDER_CONFIG)
    parser.add_argument("--keiya-target", action="append", default=[], help="Skill that should exist in Keiya")
    parser.add_argument("--galyarder-target", action="append", default=[], help="Skill that should exist in Galyarder")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    inv = {
        "keiya": scan(args.keiya_root, args.keiya_config),
        "galyarder": scan(args.galyarder_root, args.galyarder_config),
    }
    keiya_names = set(inv["keiya"]["items"])
    galyarder_names = set(inv["galyarder"]["items"])
    shared = keiya_names & galyarder_names

    checks = {
        "keiya_targets_missing": [name for name in args.keiya_target if name not in keiya_names],
        "galyarder_targets_missing": [name for name in args.galyarder_target if name not in galyarder_names],
    }
    summary = {
        "keiya_total": len(keiya_names),
        "keiya_enabled": sum(1 for name in keiya_names if inv["keiya"]["items"][name]["enabled"]),
        "keiya_disabled_config": len(inv["keiya"]["disabled"]),
        "keiya_valid_disabled": len(inv["keiya"]["valid_disabled"]),
        "keiya_unmatched_disabled": inv["keiya"]["unmatched_disabled"],
        "keiya_duplicates": len(inv["keiya"]["duplicates"]),
        "keiya_bad_frontmatter": len(inv["keiya"]["bad_frontmatter"]),
        "keiya_hub_lock": len(inv["keiya"]["lock"]),
        "galyarder_total": len(galyarder_names),
        "galyarder_enabled": sum(1 for name in galyarder_names if inv["galyarder"]["items"][name]["enabled"]),
        "galyarder_disabled_config": len(inv["galyarder"]["disabled"]),
        "galyarder_valid_disabled": len(inv["galyarder"]["valid_disabled"]),
        "galyarder_unmatched_disabled": inv["galyarder"]["unmatched_disabled"],
        "galyarder_duplicates": len(inv["galyarder"]["duplicates"]),
        "galyarder_bad_frontmatter": len(inv["galyarder"]["bad_frontmatter"]),
        "galyarder_hub_lock": len(inv["galyarder"]["lock"]),
        "shared": len(shared),
        "keiya_only": len(keiya_names - galyarder_names),
        "galyarder_only": len(galyarder_names - keiya_names),
    }
    report = {
        "summary": summary,
        "checks": checks,
        "provenance_counts": {
            "keiya_only": dict(Counter(provenance(inv["keiya"], name) for name in keiya_names - galyarder_names)),
            "galyarder_only": dict(Counter(provenance(inv["galyarder"], name) for name in galyarder_names - keiya_names)),
        },
        "keiya_only_by_category": group_by_category(inv["keiya"], keiya_names - galyarder_names),
        "galyarder_only_by_category": group_by_category(inv["galyarder"], galyarder_names - keiya_names),
        "duplicates": {label: data["duplicates"] for label, data in inv.items()},
        "bad_frontmatter": {label: data["bad_frontmatter"] for label, data in inv.items()},
    }

    failures: list[str] = []
    for label in ("keiya", "galyarder"):
        if inv[label]["duplicates"]:
            failures.append(f"{label} duplicates: {sorted(inv[label]['duplicates'])}")
        if inv[label]["bad_frontmatter"]:
            failures.append(f"{label} bad frontmatter: {inv[label]['bad_frontmatter'][:5]}")
        if inv[label]["unmatched_disabled"]:
            failures.append(f"{label} unmatched disabled: {inv[label]['unmatched_disabled']}")
    if checks["keiya_targets_missing"]:
        failures.append(f"keiya targets missing: {checks['keiya_targets_missing']}")
    if checks["galyarder_targets_missing"]:
        failures.append(f"galyarder targets missing: {checks['galyarder_targets_missing']}")

    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"summary": summary, "checks": checks, "failures": failures}, indent=2, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
