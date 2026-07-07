# Hermes Profile Skill Normalization

Session learning from normalizing all `galyarder-framework` skills into Hermes Agent style.

## Problem

A large imported skill pack can be technically readable but not Hermes-native:

- frontmatter names are display labels (`Design System: Apple`) instead of Hermes-safe slugs
- directory names do not match frontmatter names
- old platform boilerplate is repeated in every skill body
- missing `version`, `author`, `license`, or `metadata.hermes.tags`
- `skills.disabled` in `config.yaml` can contain old names and hide/mislead loader checks
- current-session `skill_view` may use a cached/older index until reload/reset

## Safe normalization workflow

1. Inventory first:
   - count `*/SKILL.md`
   - parse YAML frontmatter
   - compare directory name vs `frontmatter.name`
   - detect duplicate boilerplate blocks
   - detect disabled names in active profile config
2. Back up before writes under profile-local backup path, not repo root.
3. Normalize frontmatter only:
   - `name`: lowercase slug, max 64 chars, filesystem-safe
   - `description`: starts with `Use when`, trigger-focused, under 1024 chars
   - add `version`, `author`, `license`
   - add `metadata.hermes.tags` and compact `related_skills` when useful
4. Remove old global boilerplate from bodies, but keep domain-specific content intact.
5. Rename directories that mismatch the new slug so `skill_view(<slug>)` can resolve directly.
6. Validate using both methods:
   - direct parser/validator over every `SKILL.md`
   - Hermes loader under the active profile, e.g. `HERMES_HOME=/path/to/profile python -c 'from tools.skills_tool import _find_all_skills; ...'`
7. Test representative skills with `skill_view`: one normal skill, one renamed directory skill, one always-loaded governance skill.
8. Do not re-enable disabled skills unless the user explicitly asks; style migration and runtime enablement are separate operations.

## Profile-to-profile parity cleanup

When the default Hermes home and a named profile have diverged skill libraries, treat them as two separate runtime stores, not one broken folder:

1. Resolve both roots explicitly, for example `/home/galyarder/.hermes/skills` and `/home/galyarder/.hermes/profiles/galyarder/skills`.
2. Inventory `SKILL.md` files by frontmatter `name`, relative path, category, and duplicate names. Compare by skill name first; directory taxonomy can intentionally differ.
3. Sync only class-level missing skills in both directions after confirming they are broadly useful. Do not blindly mirror every archived or persona-specific file.
4. Watch `.archive` under active `skills/`: Hermes can still scan `SKILL.md` files there. Move duplicate archive trees outside active `skills/` (for example to a profile-local `tmp/skill-sync-backup-*`) or remove/rename their `SKILL.md` if they should not load.
5. For persona/media skills, verify profile-local asset paths. In the Galyarder profile, image references live under `/home/galyarder/.hermes/profiles/galyarder/image_cache/`, with separate subdirs for `galyarder/` and `keiya-zeyni/`.
6. Verify after edits: both libraries have zero duplicate frontmatter names, expected only-in-one-profile deltas are intentional, and representative skills load with `skill_view`.
7. Skill stores may not be git repos. If `git rev-parse --show-toplevel` fails for the skill root, record a backup path instead of claiming a commit.
8. When the user asks to "rapihin/benerin positions", preserve intentional taxonomy differences but fix name-level parity, missing class-level skills, stale profile-specific paths, and duplicate active `SKILL.md` entries.

## Pitfalls

- `skills_list` and `skill_view` in the current conversation can disagree immediately after mass edits because of session/runtime caching. Verify through the Hermes loader with explicit `HERMES_HOME` and then reload/reset if needed.
- If frontmatter name changes but the directory does not, list output may show the new name while direct `skill_view(new-name)` fails. Rename the folder too.
- Avoid generating generic descriptions for specialized skills. A generic `Use when working on X tasks` passes validation but hurts skill discovery. Prefer hand-tuned trigger phrases for high-use classes.
- Do not treat config `skills.disabled` as a parse failure. Disabled skills can still be indexed with `skip_disabled=True`, but normal `skill_view` will refuse them.
