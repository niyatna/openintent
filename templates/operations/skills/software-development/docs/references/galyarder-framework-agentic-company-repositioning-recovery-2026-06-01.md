# Galyarder Framework agentic-company repositioning recovery (2026-06-01)

## Trigger
Use this reference when repositioning `galyarder-framework` or a similar generated MkDocs/repo-wide agent framework from older `1-Man Army` / AGI / hype posture to **Agentic Company Framework / Intelligence Layer** language, especially after an interrupted Discord session or broad local diff.

## Lessons

1. **Do not assume local/untracked files are noise.**
   - `.github/workflows/publish-npm.yml` looked unrelated during docs cleanup but was Galih's own local work.
   - If a local file is removed by mistake, search recovery surfaces before declaring loss: `git status`, `git reflog`, `git fsck --lost-found`, dangling commits, checkpoint commits, and session transcripts.
   - In this session the workflow was recovered from dangling commit `05d80e15e91308b39352c03941f9a033da3f4f41` with:
     ```bash
     git checkout 05d80e15e91308b39352c03941f9a033da3f4f41 -- .github/workflows/publish-npm.yml
     ```
   - Verify preservation with checksum when the file must remain untouched:
     ```bash
     sha256sum .github/workflows/publish-npm.yml
     ```

2. **User may intentionally broaden scope.**
   - Galih corrected that if README changes from `1-Man Army` to `Agentic Company`, then the whole codebase/docs/integrations can move to that vibe too.
   - In that case, broad changes to `agents/`, `commands/`, `skills/`, `integrations/`, `.cursor/rules`, generated docs, package metadata, and marketplace metadata can be intended.
   - Preserve identifiers such as `elite-developer` and file paths unless renaming is explicitly requested.

3. **Separate public repositioning from compatibility mappers.**
   - Public/output source should avoid old posture terms: `1-Man Army`, unexplained `AGI`, `Humans 3.0`, `Digital HQ` as marketing posture, `zero-slop`, `swarms`, `empire`, `sentient`, and `Karpathy` as marketing shorthand.
   - `scripts/generate-docs.py` may keep those strings as legacy regex mapper literals so generated docs can normalize old source text. Do not count mapper literals as public leaks unless they render into docs.

4. **Backup before broad cleanup.**
   ```bash
   env -u GIT_EXTERNAL_DIFF git --no-pager diff --binary > /tmp/galyarder-framework-full-vibe-before-finish.patch
   git status --short > /tmp/galyarder-framework-status-before-finish.txt
   ```
   Avoid `GIT_EXTERNAL_DIFF=` because this environment can interpret an empty external diff command incorrectly.

5. **Verification ladder for this class.**
   ```bash
   git diff --check
   npm test
   uvx --from mkdocs-material mkdocs build
   ```
   Then scan:
   - repo source excluding `.git`, `site`, `node_modules`, `local_cache`, `__pycache__`, and intentional mapper literals;
   - rendered `site/index.html` for `Open-source Agentic Company Framework`, `founder intent`, `Intelligence Layer`, and `agentic company`;
   - live GitHub Pages after push/deploy.

6. **Strict MkDocs is a debt detector, not necessarily a blocker.**
   `mkdocs build --strict` can fail on existing/generated broken-link warnings. Report it separately from non-strict build pass. Do not silently broaden the task into fixing all broken generated skill reference links unless asked.

## Terse status shape for Galih

```text
state: <done/partial/blocked>
- recovered/preserved: <user local file/checksum>
- broad diff: <counts/families>
- verified: <diff-check, npm test, mkdocs, scan>
- not done / gate: <commit/push/live verify or human decision>
```
