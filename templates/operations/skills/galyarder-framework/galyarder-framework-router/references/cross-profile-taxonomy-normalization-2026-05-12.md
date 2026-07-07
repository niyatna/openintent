# Cross-Profile Taxonomy Normalization — 2026-05-12

Use this as the governance note for the Keiya/default and Galyarder skill-tree cleanup after the selective cross-profile sync.

## Final state

- Keiya/default skill root: `/home/galyarder/.hermes/skills`
- Galyarder skill root: `/home/galyarder/.hermes/profiles/galyarder/skills`
- Both profiles normalized to 26 top-level categories.
- Active root/name-as-category dirs: 0 in both profiles.
- Bad YAML frontmatter: 0 in both profiles.
- Duplicate frontmatter names: 0 in both profiles.
- Unmatched disabled config entries: 0 in both profiles.
- Category metadata mismatches: 0 in both profiles.
- Path/category mismatches: 0 in both profiles.
- `.hub/lock.json` paths resolve for all remaining installed entries: Keiya 209/209, Galyarder 121/121.

## Backups

- Primary backup: `/home/galyarder/.hermes/backups/skills-taxonomy-normalization-taxonomy-20260512-171813.tar.gz`
- Repair-pass backup: `/home/galyarder/.hermes/backups/skills-taxonomy-normalization-taxonomy-repair-20260512-171946.tar.gz`

## Artifacts

- Final report: `/tmp/skill_taxonomy_normalization_final_summary.md`
- Final taxonomy verifier: `/tmp/skill_taxonomy_normalization_verify_final2-20260512-173306.json`
- Final cross-profile verifier: `/tmp/cross_profile_skill_sync_after_taxonomy_final.json`
- Enabled snapshots: `/tmp/keiya_skills_list_after_taxonomy.txt`, `/tmp/galyarder_skills_list_after_taxonomy.txt`

## Category policy

Use canonical broad shelves, not one-folder-per-skill community sprawl:

- `growth`
- `software-development`
- `creative`
- `design-systems`
- `gstack-workflow`
- `mlops`
- `productivity`
- `security`
- `finance-legal`
- `research`
- `galyarder-company`
- `devops`
- `qa-testing`
- `communication`
- `autonomous-ai-agents`
- `galyarder-framework`
- `media`
- `product-management`
- `note-taking`
- `galyarder-self`
- `mcp`
- `browser`
- `dogfood`
- `gaming`
- plus small shelves when present: `blockchain`, `data-science`, `red-teaming`

## Important repair discovered

Some LobeHub/community skills had malformed frontmatter where `source: lobehub---` fused the YAML closing marker into the value. Fix by replacing:

```yaml
source: lobehub---
```

with:

```yaml
source: lobehub
---
```

This affected Keiya/default and Galyarder copies of skills like `business-guru`, `flux-prompt-generator`, and other LobeHub imports. Run a parser after repairs; do not trust visual inspection.

## Lock cleanup pattern

After moving folders, update `.hub/lock.json` path fields to actual relative skill directories. Also normalize legacy lock keys to frontmatter names where possible, for example:

- `here-now` -> `here-now`
- `qdrant` -> `qdrant-vector-search`
- `stable-diffusion` -> `stable-diffusion-image-generation`
- `accelerate` -> `peft-fine-tuning`
- `peft` -> `peft-fine-tuning`
- `flash-attention` -> `serving-llms-vllm`
- `modal` -> `serving-llms-vllm`
- `lambda-labs` -> `serving-llms-vllm`
- `cli` -> `inference-sh-cli`
- `torchtitan` -> `distributed-llm-pretraining-torchtitan`
- `slime` -> `peft-fine-tuning`
- `saelens` -> `sparse-autoencoder-training`
- `simpo` -> `peft-fine-tuning`

Remove lock entries only when no active skill with matching frontmatter/path exists.

## Verification gates

Before saying taxonomy cleanup is done, run:

1. Direct parser verifier over both roots:
   - total skills
   - duplicates
   - bad frontmatter
   - disabled config validity
   - root/name-as-category count
   - category metadata/path mismatches
2. Cross-profile verifier:
   - shared count
   - Keiya-only/Galyarder-only count
   - hub lock count
   - failures empty
3. CLI smoke:
   - `hermes --profile default skills list --enabled-only`
   - `hermes --profile galyarder skills list --enabled-only`
   - one-shot chat smoke for both profiles with `chat -Q -q ... --ignore-rules --max-turns 1`
4. Runtime skill smoke:
   - `skill_view` on representative moved skills.
   - `skills_list(category=...)` on representative categories.

Do not rely on the current conversation's cached skill index alone after mass edits.
