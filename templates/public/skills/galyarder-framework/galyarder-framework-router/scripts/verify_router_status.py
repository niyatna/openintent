#!/usr/bin/env python3
"""Verify Galyarder profile skill router readiness after V2.1 taxonomy normalization.

Checks profile-local skills, router references, critical trigger strings,
representative routing scenarios, and the generated inventory references.
"""
from __future__ import annotations

from pathlib import Path
import os
import re
import sys
import yaml
from collections import Counter, defaultdict

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_DIR = _SCRIPT_DIR.parent
_GF_DIR = _SKILL_DIR.parent
_PROFILE_SKILLS = _GF_DIR.parent
ROOT = Path(os.environ.get("GALYARDER_SKILLS_ROOT", _PROFILE_SKILLS)).resolve()

ROUTER = ROOT / "galyarder-framework" / "galyarder-framework-router" / "SKILL.md"
ROUTER_REF = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "current-local-skill-inventory.md"
CORE_PACK = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "core-daily-pack.md"
REBUILD = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "2026-05-11-skill-routing-inventory-rebuild.md"
NOISE_AUDIT = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "v2-skill-noise-stale-audit.md"
HUB_COMPARISON = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "v2-fresh-hub-comparison.md"
ARCHIVE_PLAN = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "v2-stale-skill-archive-plan.md"
SEPARATE_SESSION = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "v2-separate-session-verification.md"
CROSS_PROFILE = ROOT / "galyarder-framework" / "galyarder-framework-router" / "references" / "cross-profile-merge-patterns.md"

REQUIRED_SKILLS = {
    "galyarder-framework-router": ["canonical router", "bounce", "pi-cli", "claude-code", "opencode", "codex", "core-daily-pack", "v2.1.0", "domain routing map", "pre-flight checklist", "direct-command", "curated skill stack", "v2-skill-noise-stale-audit", "v2-fresh-hub-comparison", "v2-stale-skill-archive-plan", "profile-local taxonomy normalization"],
    "using-galyarder-framework": ["galyarder-framework-router", "Direct Command Override", "Skill tool"],
    "keiya-capability-router": ["Keiya Capability Router", "Escalation To Galyarder", "galyarder-framework-router"],
    "discord": ["Controlled relay protocol", "raw Discord mention"],
    "hermes": ["Use when configuring, extending, troubleshooting, or packaging Hermes Agent"],
}

SCENARIOS = {
    "coding feature": ["implement fitur X", "Pi", "Claude Code", "OpenCode", "Codex"],
    "Hermes runtime bug": ["hermes", "verification"],
    "Google Workspace auth contradiction": ["Google Workspace auth contradiction", "google-workspace", "gws"],
    "ordinary finance": ["Ordinary finance", "galyarder-financial-services-workflows", "financial-analyst"],
    "Ledger finance": ["Galyarder Ledger finance workflow", "galyarder-financial-services-workflows"],
    "Obsidian vault": ["Obsidian vault", "obsidian"],
    "emotional state": ["Emotional state", "keiya-capability-router", "keiya-presence-memory"],
}

def parse_frontmatter(path: Path):
    text = path.read_text(errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text, False
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}, text, False
    return fm, text, "name" in fm and "description" in fm and len(str(fm.get("description", ""))) <= 1024

def main() -> int:
    failures: list[str] = []
    skill_files = sorted(ROOT.rglob("SKILL.md"))
    if not skill_files:
        failures.append("no SKILL.md files found")

    names: defaultdict[str, list[str]] = defaultdict(list)
    top_categories: Counter[str] = Counter()
    bad_frontmatter: list[str] = []
    for path in skill_files:
        fm, _text, ok = parse_frontmatter(path)
        name = str(fm.get("name", path.parent.name))
        names[name].append(str(path))
        rel = path.relative_to(ROOT)
        top_categories[rel.parts[0]] += 1
        if not ok:
            bad_frontmatter.append(str(path))

    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}
    if duplicates:
        failures.append(f"duplicate skill names: {duplicates}")
    if bad_frontmatter:
        failures.append(f"bad frontmatter/description: {bad_frontmatter[:10]}")
    if len(skill_files) < 100:
        failures.append(f"unexpectedly low skill count: {len(skill_files)}")
    if len(top_categories) < 20:
        failures.append(f"unexpectedly low top-level category count: {len(top_categories)}")

    required_files = [ROUTER, ROUTER_REF, CORE_PACK, REBUILD, NOISE_AUDIT, HUB_COMPARISON, ARCHIVE_PLAN, SEPARATE_SESSION, CROSS_PROFILE]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing required file: {path}")

    for skill, needles in REQUIRED_SKILLS.items():
        paths = names.get(skill, [])
        if not paths:
            failures.append(f"missing required skill: {skill}")
            continue
        text = Path(paths[0]).read_text(errors="replace").lower()
        for needle in needles:
            if needle.lower() not in text:
                failures.append(f"{skill} missing trigger: {needle}")

    if ROUTER.exists():
        router_text = ROUTER.read_text(errors="replace").lower()
        for scenario, needles in SCENARIOS.items():
            for needle in needles:
                if needle.lower() not in router_text:
                    failures.append(f"router scenario '{scenario}' missing: {needle}")

    if CORE_PACK.exists():
        core_text = CORE_PACK.read_text(errors="replace")
        for needle in ["Do not load this whole pack", "pi-cli", "google-workspace", "keiya-presence-memory", "Profile-local normalization note"]:
            if needle not in core_text:
                failures.append(f"core daily pack missing: {needle}")

    if ROUTER_REF.exists():
        ref_text = ROUTER_REF.read_text(errors="replace")
        for needle in ["Total active profile skills: 117", "Top-level categories: 24", "Full inventory pointer"]:
            if needle not in ref_text:
                failures.append(f"router inventory ref missing: {needle}")

    if NOISE_AUDIT.exists():
        noise_text = NOISE_AUDIT.read_text(errors="replace")
        for needle in ["Active profile skills: **117**", "Exact duplicate skill names: **0**", "No skills were deleted", "Router preference rules"]:
            if needle not in noise_text:
                failures.append(f"noise audit missing: {needle}")

    if HUB_COMPARISON.exists():
        hub_text = HUB_COMPARISON.read_text(errors="replace")
        for needle in ["684 total skills", "Local active profile inventory: **117 skills**", "No hub installs were performed", "optional expansions"]:
            if needle not in hub_text:
                failures.append(f"hub comparison missing: {needle}")

    if ARCHIVE_PLAN.exists():
        archive_text = ARCHIVE_PLAN.read_text(errors="replace")
        for needle in ["non-destructive", "explicit approval", "Compatibility shims", "skill_manage(action=\"delete\"", "V2.1 normalization execution note"]:
            if needle not in archive_text:
                failures.append(f"archive plan missing: {needle}")

    if REBUILD.exists():
        rebuild_text = REBUILD.read_text(errors="replace")
        for needle in ["V2 final pass", "V2 final / non-destructive", "No skill was deleted", "V2.1 profile-local taxonomy normalization", "No SKILL.md `name:` values were changed"]:
            if needle not in rebuild_text:
                failures.append(f"rebuild reference missing: {needle}")

    if SEPARATE_SESSION.exists():
        separate_text = SEPARATE_SESSION.read_text(errors="replace")
        for needle in ["SEPARATE_SESSION_VERIFICATION=PASS", "V2 final / non-destructive", "skill_view", "verify_router_status.py"]:
            if needle not in separate_text:
                failures.append(f"separate-session verification missing: {needle}")
    else:
        failures.append(f"missing separate-session verification log: {SEPARATE_SESSION}")

    print(f"root={ROOT}")
    print(f"skills={len(skill_files)}")
    print(f"top_categories={len(top_categories)}")
    print(f"duplicate_skill_names={len(duplicates)}")
    print(f"bad_frontmatter={len(bad_frontmatter)}")
    print(f"core_daily_pack={'yes' if CORE_PACK.exists() else 'no'}")
    print(f"v2_noise_audit={'yes' if NOISE_AUDIT.exists() else 'no'}")
    print(f"v2_fresh_hub_comparison={'yes' if HUB_COMPARISON.exists() else 'no'}")
    print(f"v2_stale_archive_plan={'yes' if ARCHIVE_PLAN.exists() else 'no'}")
    print(f"separate_session_verification={'yes' if SEPARATE_SESSION.exists() else 'no'}")
    print(f"required_router_files={'yes' if all(p.exists() for p in required_files) else 'no'}")
    print("status=V2.1 profile-local normalized / non-destructive")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
