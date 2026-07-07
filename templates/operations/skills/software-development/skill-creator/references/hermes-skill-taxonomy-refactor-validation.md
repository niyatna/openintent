# Hermes Skill Taxonomy Refactor Validation

Use this when reorganizing many Hermes profile skills into category/domain folders or changing a router/orchestration layer.

## Trigger

A session moved many `SKILL.md` files, introduced/changed a canonical router, or split a large skill bucket into class-level domain folders such as `engineering`, `product`, `finance`, `marketing`, `legal-risk`, `security`, `knowledge`, `creative`, and `operations`.

## Safe workflow

1. Back up the active profile skill tree before edits.
   - Put the archive under the active profile, e.g. `$HERMES_HOME/backups/skills-before-<change>.tar.gz`.
   - Do not rely on git; profile skill stores may not be git repos.
2. Move files by frontmatter `name`, not only directory names.
   - Build an old name -> old path map from the backup.
   - Build a current name -> current path map after moves.
3. Patch the orchestration layer.
   - Keep the framework/router folder for routing, doctrine, decision logs, and compatibility aliases.
   - Move domain specialists into domain folders.
   - Mark old canonical routers as legacy aliases if kept for compatibility.
4. Sync `metadata.hermes.category` for every moved skill.
   - Category should match the top-level folder unless the runtime intentionally supports another namespace.
   - Mass move often leaves valid frontmatter with stale or missing category metadata.
5. Check active profile config.
   - Remove stale disabled entries only when the goal is to reactivate those skills.
   - Verify `disabled_skills` is empty or intentional before claiming loadability.
6. Validate all skills.
   - YAML frontmatter parses.
   - Required `name` and `description` exist.
   - Active skill names are unique.
   - Explicit category values match folders.
   - Moved skills have category metadata.
7. Validate router references.
   - Extract backticked skill-looking tokens from router docs.
   - Every referenced skill must exist or be clearly described as a tool/category/product term, not a missing skill.
   - Remove or reword stale pseudo-skill references such as a generic `research` token when no such skill exists.
8. Validate loadability with the live skill tool.
   - Load the router itself.
   - Load representative skills from each affected category.
   - Use `skills_list(category=...)` for domain shelf counts.
9. Validate scenario routes.
   - Test examples across the intended taxonomy, e.g. finance modeling, product PRD, failing tests, weekly strategy, launch campaign, contract review, and security review.
   - For each scenario, verify primary/support skill names resolve to actual paths.
10. Update governing docs and aliases.
   - Patch fallback routers and doctrine docs so they point to the new canonical router and taxonomy.
   - Compatibility aliases should explicitly say which router now wins.

## Minimal validation report

Report these fields before claiming completion:

```text
status: PASS/FAIL
skills_total:
backup_exists:
frontmatter_errors_count:
duplicate_names_count:
explicit_category_mismatches_count:
moved_count:
moved_missing_category_count:
moved_category_mismatch_count:
router_missing_refs_count:
disabled_skills_count:
required_category_counts:
scenario_missing:
```

Only say PASS when all failure counts are zero, required category counts are non-zero, and the router plus representative domain skills loaded through `skill_view`.

## Pitfalls

- A mass move can look successful while `metadata.hermes.category` remains missing on most moved skills.
- `skills_list` can show categories by folder even when frontmatter category metadata is incomplete; verify both.
- Current-session tooling may cache skill indexes after large edits. Use direct file parsing plus live `skill_view` on representative skills.
- Do not delete compatibility routers immediately after a refactor. Mark them legacy first, then remove only after all references are known clean.
- Router docs often contain backticked words that are not skills. Reword ambiguous tokens or whitelist deliberate non-skill terms so future validation is clean.
- If `git -C $HERMES_HOME status` fails, do not claim a git diff. Report the backup archive path instead.
