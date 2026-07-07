# Cross-Profile Skill Governance

Use this when Galih asks to compare, sync, or clean the Keiya/default and Galyarder skill libraries without turning them into noisy clones.

## Roots

- Keiya/default shared skill root: `/home/galyarder/.hermes/skills`
- Galyarder profile skill root: `/home/galyarder/.hermes/profiles/galyarder/skills`
- Keiya config: `/home/galyarder/.hermes/config.yaml`
- Galyarder config: `/home/galyarder/.hermes/profiles/galyarder/config.yaml`

Always verify live paths before editing. Hermes profile `$HOME` can be profile-local, so do not infer the active skill root from `~` alone.

## Policy

Do not force full parity.

Use this split:

- **Shared both ways:** procedural/tool skills that improve both profiles without changing posture.
- **Keiya-only:** presence, playful, companion, broad persona, translation, and everyday assistant skills.
- **Galyarder-only:** company execution, Galyarder Labs doctrine, Ledger/HQ, finance infrastructure, audit, operator, and mission skills.
- **LobeHub/community:** advisory taste/market/culture layers only; never authority for legal, finance, security, external sends, or doctrine.

If a diff is large, select a small high-value sync set. Full syncing hundreds of skills usually makes routing worse.

## Non-Destructive Sync Workflow

1. **Backup first**
   ```bash
   TS=$(date +%Y%m%d-%H%M%S)
   BACKUP="/home/galyarder/.hermes/tmp/cross-profile-skill-sync-$TS"
   mkdir -p "$BACKUP/locks"
   cp -a /home/galyarder/.hermes/config.yaml "$BACKUP/keiya-config.yaml"
   cp -a /home/galyarder/.hermes/profiles/galyarder/config.yaml "$BACKUP/galyarder-config.yaml"
   cp -a /home/galyarder/.hermes/skills/.hub/lock.json "$BACKUP/locks/keiya-lock.json" 2>/dev/null || true
   cp -a /home/galyarder/.hermes/profiles/galyarder/skills/.hub/lock.json "$BACKUP/locks/galyarder-lock.json" 2>/dev/null || true
   ```

2. **Inventory by frontmatter `name`, not folder slug**
   - Exclude `.hub/` and `.archive/`.
   - Parse YAML frontmatter.
   - Track duplicates by `name`.
   - Track `skills.disabled` entries from config.

3. **Copy only selected missing skills**
   - Preserve the source relative directory when possible.
   - If destination directory exists but frontmatter name is missing, use a safe `-synced` suffix instead of overwriting.
   - Copy supporting `references/`, `templates/`, `scripts/`, and `assets/` together with `SKILL.md`.
   - Update `.hub/lock.json` only for copied hub-installed skills and only if the destination lock lacks that key.

4. **Fix disabled config mismatch**
   - Keiya may contain disabled entries like `Design System: Stripe` while the actual skill name/folder is `design-system-stripe`.
   - Map `Design System: X` to `design-system-<slug(x)>` if that skill exists.
   - Remove stale unmatched design-system aliases only after verifying no matching skill exists.
   - Verification target: `unmatched_disabled == []` for both profiles.

5. **Repair frontmatter discovered by verification**
   - Common community/LobeHub failure: unquoted `description:` values containing `:`.
   - Example bad YAML:
     ```yaml
     description: Business Consultant: Providing support
     ```
   - Repair after backup by quoting the scalar:
     ```yaml
     description: "Business Consultant: Providing support"
     ```
   - Re-run YAML parsing after repair.

6. **Handle duplicate skill names safely**
   - Prefer canonical class-level skill over community/root duplicate.
   - Move the duplicate outside the active skill tree, e.g.:
     ```text
     /home/galyarder/.hermes/profiles/galyarder/tmp/skill-sync-backup-YYYYMMDD-duplicate-<name>/<name>/
     ```
   - If the duplicate has a stale `.hub/lock.json` entry, remove only that entry after backup.

7. **Verify before reporting**
   Required gates:
   - selected sync targets present in destination
   - duplicate names: `0`
   - bad frontmatter: `0`
   - unmatched disabled entries: `0`
   - smoke parse selected synced skill names

## 2026-05-12 Governance Pass Pattern

A successful pass synced a small curated set instead of all profile-only skills:

- Keiya → Galyarder: copy/distribution/dev-doc/security skills (`discord-copywriting`, `facebook-ads-expert`, `seo-helper`, `api-docs-writer`, `architect`, `typescript-developer`, `fastapi-development`, `linux-shell-assistant`, `commit-assistant`, `github-doc-asst`, `cyber-specialist`, etc.).
- Galyarder → Keiya: practical ops/research/vault skills (`watchers`, `github-pr-workflow`, `api-discovery`, `scrapling`, `scrapling`, `stocks`, Obsidian pack, `obsidian`).

Verification ended with zero duplicates, zero bad frontmatter, zero unmatched disabled entries, and all selected sync targets present.

## Reusable Pitfalls

- CLI/hub lock state is not enough. Verify actual `SKILL.md` frontmatter names.
- Exact-name diff can overstate capability gaps when taxonomy differs; inspect category/path and frontmatter before syncing.
- Disabled config can look large but be ineffective if names are display labels instead of skill slugs.
- Repairing YAML frontmatter may reveal true duplicates that were hidden by parse failures.
- Do not let community/LobeHub duplicates override stronger class-level local skills.

## Script Pointer

Use `scripts/verify_cross_profile_skill_sync.py` as the reusable verifier for both profile roots. It checks inventory, duplicates, bad frontmatter, disabled entries, selected sync targets, and post-sync diff summary.
