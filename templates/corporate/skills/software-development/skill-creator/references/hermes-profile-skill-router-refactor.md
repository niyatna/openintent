# Hermes Profile Skill Router Refactor Notes

Use these notes when reorganizing Galyarder/Keiya skills, router skills, or domain taxonomy across Hermes profiles.

## Session lesson

A Galyarder profile skill refactor can pass locally while the default Keiya profile still has stale router state. In this session, the Galyarder profile had the new `galyarder-framework-router` and domain folders, but the default `~/.hermes/skills` tree still lacked that router and still referenced `galyarder-specialist` from `using-galyarder-framework`, `keiya-capability-router`, and Seneth.

Do not treat one profile's skill tree as proof that the Keiya/default profile is current.

## Required validation after router/taxonomy refactors

1. Identify both skill roots:
   - Galyarder profile: `/home/galyarder/.hermes/profiles/galyarder/skills`
   - Default/Keiya profile: `/home/galyarder/.hermes/skills`
2. Check all changed router skills load via `skill_view` in the active profile.
3. Parse every `SKILL.md` frontmatter in the active profile.
4. Check duplicate `name` values.
5. Check explicit `metadata.hermes.category` values match folder names for moved skills.
6. Check router backtick references point to existing skill names.
7. Run scenario route checks for representative work.
8. Compare key router skills across both skill roots and record sync gaps.
9. Patch loaded router skills immediately when references are stale.
10. If default/Keiya is intentionally not synced, record that as an explicit operational gap, not as success.

## Minimal verification script

Run from any directory with Python/PyYAML available:

```python
from pathlib import Path
import re, yaml, json

roots = {
    "keiya_default": Path("/home/galyarder/.hermes/skills"),
    "galyarder": Path("/home/galyarder/.hermes/profiles/galyarder/skills"),
}
keys = [
    "keiya-capability-router",
    "galyarder-framework-router",
    "seneth-council-router",
    "using-galyarder-framework",
    "galyarder-financial-services-pack",
    "galyarder-financial-services-workflows",
    "galyarder-ceo",
    "galyarder-cfo-coo",
]

def scan(root):
    out = {"exists": root.exists(), "count": 0, "keys": {}, "duplicates": {}, "frontmatter_errors": []}
    if not root.exists():
        return out
    by_name = {}
    for p in root.glob("**/SKILL.md"):
        text = p.read_text(errors="replace")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not m:
            out["frontmatter_errors"].append(str(p.relative_to(root)))
            continue
        try:
            data = yaml.safe_load(m.group(1)) or {}
        except Exception as e:
            out["frontmatter_errors"].append(f"{p.relative_to(root)}: {e}")
            continue
        name = data.get("name")
        if not name:
            out["frontmatter_errors"].append(f"{p.relative_to(root)}: missing name")
            continue
        rel = str(p.relative_to(root))
        by_name.setdefault(name, []).append(rel)
        out["count"] += 1
        if name in keys:
            folder = rel.split("/")[0]
            hermes = ((data.get("metadata") or {}).get("hermes") or {}) if isinstance(data.get("metadata") or {}, dict) else {}
            out["keys"][name] = {
                "path": rel,
                "folder": folder,
                "category": hermes.get("category") if isinstance(hermes, dict) else None,
                "mentions_framework_router": "galyarder-framework-router" in text,
                "mentions_specialist": "galyarder-specialist" in text,
            }
    out["duplicates"] = {k: v for k, v in by_name.items() if len(v) > 1}
    return out

print(json.dumps({name: scan(root) for name, root in roots.items()}, indent=2))
```

## Scenario route set

Use these to pressure-test the Keiya/Galyarder split:

- `Keiya, bantu bikin DCF dari file ini` -> `keiya-capability-router` -> `galyarder-financial-services-pack` + `financial-analyst`
- `design Ledger CFO Agent workflow` -> `galyarder-framework-router` -> `galyarder-financial-services-workflows` + `galyarder-cfo-coo` + product skill
- `aku capek, bantu rapihin pikiran` -> Keiya/Seneth first; stabilize before business router
- `best move Galyarder Labs minggu ini apa?` -> `galyarder-framework-router` -> `business-strategy-operator` + `galyarder-ceo` + maybe `business-strategy-operator`
- `fix failing tests di repo` -> `galyarder-framework-router` -> engineering debugging/verification skills

## Pitfalls

- Do not assume profile-local changes update default Keiya skills.
- Do not leave active router docs pointing to legacy `galyarder-specialist` except where explicitly documented as compatibility alias.
- Do not validate only file moves; validate loadability and scenario routing.
- Do not create narrow one-session skills for router migrations; patch class-level router/skill-authoring skills and add a reference note like this.

## Useful backup pattern

Before broad skill moves:

```bash
tar -czf /home/galyarder/.hermes/profiles/galyarder/backups/skills-before-router-refactor-$(date -u +%Y%m%dT%H%M%SZ).tar.gz \
  -C /home/galyarder/.hermes/profiles/galyarder skills
```
