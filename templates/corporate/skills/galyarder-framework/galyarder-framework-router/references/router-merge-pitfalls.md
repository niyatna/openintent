# Router Merge Pitfalls — v1.2.0 → v2.1.0 (2026-05-11)

## Context

During V1→V2 merge, several non-obvious issues surfaced. These apply whenever the router, verifier, or skill resolution is modified.

## Pitfalls

### 1. Verifier `Path.home()` Redirect in Profile Context

In Hermes profile context, `Path.home()` resolves to the profile-local home:
```
/home/galyarder/.hermes/profiles/galyarder/home
```
Not the OS-level home (`/home/galyarder`). This means `Path.home() / ".hermes" / "skills"` points to a non-existent path.

**Fix:** Verifier script walks up from its own `__file__` location to find the actual skills directory, with hardcoded fallback to `/home/galyarder/.hermes/skills`.

### 2. Verifier Case-Sensitivity

`needle not in text` is case-sensitive in Python. Router uses "Domain Routing Map" (capitalized), but verifier needle was lowercase "domain routing map".

**Fix:** Both `text` and `needle` lowercased before comparison in the `REQUIRED_SKILLS` and `SCENARIOS` checks.

### 3. Scenario Needles Must Match Actual Skill Names

Verifier scenarios referenced `galyarder-financial-services-pack` but the actual skill is `galyarder-financial-services-workflows`. Similarly, `google-workspace` doesn't exist as a skill — it was text in the router but not a real skill name.

**Fix:** Cross-reference scenario needles against actual `skill_manage` inventory before writing.

### 4. Version String Format

Verifier needle `v2.1.0` won't match frontmatter `version: 2.1.0` (missing the `v` prefix). Adding `status: V2.1.0 final / non-destructive` field resolves this.

**Fix:** Always include a `status:` field in frontmatter that contains the version string in the format the verifier expects.

### 5. Sync Both Locations

Galyarder profile has dual skill locations:
- Profile-local: `$PROFILE_HOME/skills/galyarder-framework/...`
- Shared: `/home/galyarder/.hermes/skills/galyarder-framework/...`

Any change must be synced to both. Verifier scans shared; `skill_view` in galyarder profile context scans profile-local.

## Safe Merge Pattern

1. Edit profile-local SKILL.md
2. Sync to shared: `cp profile-local/SKILL.md shared/SKILL.md`
3. If verifier exists, sync that too
4. Run verifier: `python3 scripts/verify_router_status.py`
5. Verify PASS before declaring done
