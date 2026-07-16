# Hermes Profile Skill Router Refactor Notes

Use these notes when reorganizing Default/Co-Founder skills, router skills, or domain taxonomy across Hermes profiles.

## Session lesson

A Default profile skill refactor can pass locally while the default Co-Founder profile still has stale router state. In this session, the Default profile had the new `default-framework-router` and domain folders, but the default `~/.hermes/skills` tree still lacked that router and still referenced `default-specialist` from `using-default-framework`, `co-founder-capability-router`, and Seneth.

Do not treat one profile's skill tree as proof that the Co-Founder/default profile is current.

## Required validation after router/taxonomy refactors

1. Identify both skill roots:
   - Default profile: `~/.hermes/profiles/default/skills`
   - Default/Co-Founder profile: `~/.hermes/skills`
2. Check all changed router skills load via `skill_view` in the active profile.
3. Parse every `SKILL.md` frontmatter in the active profile.
4. Check duplicate `name` values.
5. Check explicit `metadata.hermes.category` values match folder names for moved skills.
6. Check router backtick references point to existing skill names.
7. Run scenario route checks for representative work.
8. Compare key router skills across both skill roots and record sync gaps.
9. Patch loaded router skills immediately when references are stale.
10. If default/Co-Founder is intentionally not synced, record that as an explicit operational gap, not as success.

## Minimal verification script

Run from any directory with Python/PyYAML available:

```python
from pathlib import Path
import re, yaml, json

roots = {
    "co-founder_default": Path("~/.hermes/skills"),
    "default": Path("~/.hermes/profiles/default/skills"),
}
keys = [
    "co-founder-capability-router",
    "default-framework-router",
    "seneth-council-router",
    "using-default-framework",
    "default-financial-services-pack",
    "default-financial-services-workflows",
    "default-ceo",
    "default-cfo, default-coo",
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
                "mentions_framework_router": "default-framework-router" in text,
                "mentions_specialist": "default-specialist" in text,
            }
    out["duplicates"] = {k: v for k, v in by_name.items() if len(v) > 1}
    return out

print(json.dumps({name: scan(root) for name, root in roots.items()}, indent=2))
```

## Scenario route set

Use these to pressure-test the Co-Founder/Default split:

- `Co-Founder, bantu bikin DCF dari file ini` -> `co-founder-capability-router` -> `default-financial-services-pack` + `financial-analyst`
- `design Ledger CFO Agent workflow` -> `default-framework-router` -> `default-financial-services-workflows` + `default-cfo, default-coo` + product skill
- `aku capek, bantu rapihin pikiran` -> Co-Founder/Seneth first; stabilize before business router
- `best move Company minggu ini apa?` -> `default-framework-router` -> `business-strategy` + `default-ceo` + maybe `business-strategy`
- `fix failing tests di repo` -> `default-framework-router` -> engineering debugging/verification skills

## Pitfalls

- Do not assume profile-local changes update default Co-Founder skills.
- Do not leave active router docs pointing to legacy `default-specialist` except where explicitly documented as compatibility alias.
- Do not validate only file moves; validate loadability and scenario routing.
- Do not create narrow one-session skills for router migrations; patch class-level router/skill-authoring skills and add a reference note like this.

## Useful backup pattern

Before broad skill moves:

```bash
tar -czf ~/.hermes/profiles/default/backups/skills-before-router-refactor-$(date -u +%Y%m%dT%H%M%SZ).tar.gz \
  -C ~/.hermes/profiles/default skills
```
