# Cross-Profile Skill Merge Patterns

## Problem

Skills can exist in two locations:
1. **Shared skills**: `/home/galyarder/.hermes/skills/` — base library (360+ skills)
2. **Profile-local skills**: `/home/galyarder/.hermes/profiles/galyarder/skills/` — profile additions/overrides

When two operators (e.g., Keiya on default profile, Galyarder on galyarder profile) independently patch the same skill, the versions diverge. Neither is "wrong" — they may have complementary features.

## Merge Strategy (Non-Destructive)

1. **Backup first** — copy current version to `<skill-name>-backup-<old-version>-<date>/`
2. **Read both versions** — identify what each has that the other doesn't
3. **Merge, don't overwrite** — create a version that includes features from BOTH
4. **Bump version** — if V1 had X and V2 had Y, merged = V2.1 (not V1 or V2)
5. **Sync to BOTH locations** — copy merged SKILL.md + all references/scripts to shared AND profile-local
6. **Run verifier** — must PASS before declaring done

## Example: Router v1.2.0 + V2 → v2.1.0

| Feature | V1.2.0 (Galyarder) | V2 (Keiya) | Merged v2.1.0 |
|---------|-------------------|------------|---------------|
| Domain routing map (10 domains) | ✅ | ❌ | ✅ |
| Pre-flight checklist | ✅ | ❌ | ✅ |
| Direct-command escape hatch | ✅ | ❌ | ✅ |
| Curated skill stack (34) | ✅ | ❌ | ✅ |
| Router-first principle | ❌ | ✅ | ✅ |
| Bounce-back enforcement | ❌ | ✅ | ✅ |
| Category scan (360 skills) | ❌ | ✅ | ✅ |
| Candidate validation | ❌ | ✅ | ✅ |
| Keiya/Galyarder posture split | ❌ | ✅ | ✅ |
| V2 references (core daily pack, audits) | ❌ | ✅ | ✅ |
| Common routing scenarios | ❌ | Partial | ✅ |

## Verifier Case-Sensitivity Pitfall

Verifier scripts that check for needle strings in SKILL.md content MUST use case-insensitive matching:

```python
# WRONG — breaks when router uses "Domain Routing Map" (Title Case)
if needle not in text:
    failures.append(...)

# CORRECT — works regardless of case
if needle.lower() not in text.lower():
    failures.append(...)
```

This hit us during the v2.1.0 merge: verifier checked for "domain routing map" (lowercase) but router had "## Domain Routing Map" (Title Case). 5 false failures.

## Sync Checklist

After any skill merge:
- [ ] Merged SKILL.md copied to shared location
- [ ] Merged SKILL.md copied to profile-local location
- [ ] All references/ copied to both locations
- [ ] All scripts/ copied to both locations
- [ ] Verifier script path-aware (see `hermes` → `profile-path-resolution-gotchas.md`)
- [ ] Verifier PASS on both locations
- [ ] Memory updated with new version status
