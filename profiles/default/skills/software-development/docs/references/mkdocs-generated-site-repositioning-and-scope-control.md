# MkDocs generated-site repositioning and scope control

Use this when a public MkDocs docs site is generated from repo source files and the user asks to reposition the whole docs surface, not only the README.

## Core lesson

A docs-site rewrite can have three different layers:

1. **Public hand-authored pages** — `docs/index.md`, `mkdocs.yml`, home overrides, quick start, workflow, navigation, and other active pages.
2. **Generated public detail pages** — `docs/agents/**`, `docs/skills/**`, `docs/commands/**`, `docs/design/**` generated from canonical source trees.
3. **Canonical runtime/source files** — repo-root `agents/**`, `skills/**`, `commands/**`, manifests, and generator scripts.

Do not treat these layers as interchangeable. README completion is not proof that GitHub Pages is repositioned. A rendered root page can remain stale even after README and repo description are correct.

## Required workflow

1. Inspect `mkdocs.yml`, deployment workflow, active nav, custom home override, and generator scripts before editing.
2. Identify which pages are authored directly and which are generated.
3. Determine the canonical source model before invoking a generator. Repos may have playwright-prod from nested plugin silos to canonical root-level `agents/`, `skills/`, and `commands/`; an outdated generator can silently delete public detail pages.
4. Preserve active slugs and IA unless the user explicitly asks for restructuring.
5. Rewrite public authored pages in place.
6. For generated public pages, prefer a generator-level public-copy sanitation/normalization step rather than bulk-mutating runtime source packages solely for marketing cleanup.
7. If the generator copies `references/`, `assets/`, or `templates/`, apply the public-copy normalization to copied Markdown support files too; sanitizing only `index.md` pages leaves stale wording in deployed references.
8. Run the generator, inspect `git status --short`, additions/deletions, and file-count parity. Unexpected mass deletions are a stop signal: diagnose generator discovery before staging.
9. Keep unrelated workflows or release automation out of a docs-only commit unless explicitly requested.
10. Stage only the intended docs/public-positioning scope. If cleanup requires destructive or restore commands and the tool asks for confirmation, stop and request approval rather than bypassing the gate.

## Verification ladder

Run fresh:

```bash
npm test
git diff --check
uvx --from mkdocs-material mkdocs build
```

Then verify:

- source pages contain the new category/mechanism language;
- rendered `site/index.html` contains the new hero and mechanism language;
- generated public docs no longer leak rejected framing;
- `git status --short` and staged diff contain only intended scope;
- GitHub Actions deploy succeeds after push;
- live GitHub Pages HTML contains the new copy after deployment.

Use `mkdocs build --strict` as a debt detector, but report it separately from regular build status. A regular build can succeed while strict mode fails on pre-existing or generated broken-link warnings. Do not collapse those into one claim.

## Failure pattern

Bad sequence:

```text
README updated -> assume GH Pages done -> run old generator blindly -> generated pages disappear -> bulk sanitize runtime source -> stage thousands of unrelated files
```

Correct sequence:

```text
inspect source model -> classify authored/generated/runtime layers -> patch public pages + generator -> regenerate -> inspect parity and scope -> build -> rendered scan -> stage narrow diff -> push -> live verify
```

## Reporting rule

When the user asks whether the docs site is already repositioned, answer the actual surface separately:

- README/repo description state;
- local docs-source state;
- local rendered MkDocs state;
- pushed commit state;
- deploy workflow state;
- live GitHub Pages state.

Do not stop after reporting `partial` if the user asked to continue the rewrite and the next action is executable. Continue until a real approval gate or blocker requires the user.
