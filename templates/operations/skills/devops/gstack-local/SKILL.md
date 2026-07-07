---
description: Use when maintaining or utilizing Garry Tan's gstack local code setups,
  verifying docker services, or triggering testing and local deployment pipelines.
metadata:
  hermes:
    category: devops
name: gstack-local
---


# gstack local

## Local install

gstack is installed from `garrytan/gstack` at:

```bash
/home/galyarder/.claude/skills/gstack
```

Verified state:

- package: `gstack` `1.26.0.0`
- repo commit at install: `bf65487`
- runtime: Bun `1.3.11`
- Claude Code present: `claude 2.1.39`
- Playwright Chromium installed and launch-tested

Convenience wrapper:

```bash
gstack-browse --help
```

The wrapper points to:

```bash
/home/galyarder/.claude/skills/gstack/browse/dist/browse
```

## Skill locations

Claude Code skills are linked under:

```bash
~/.claude/skills/
```

Hermes-readable generated skills are mirrored under:

```bash
~/.hermes/skills/gstack-workflow/
```

There are 45 gstack-workflow Hermes skills. Use `skills_list` or `skill_view` with names like:

- `gstack`
- `qa`
- `ship`
- `review`
- `office-hours`
- `writing-plans-ceo-review`
- `writing-plans-eng-review`
- `design-review`
- `cso`
- `investigate`
- `browse`

If Hermes does not show newly mirrored skills in the current session, start a fresh session or run `/reset`/gateway restart so skills are re-indexed.

## Core workflow

Use gstack for a structured software-factory loop:

1. think: `/office-hours`, `/writing-plans-ceo-review`
2. writing-plans: `/writing-plans-eng-review`, `/writing-plans-design-review`, `/autowriting-plans`
3. build/review: `/review`, `/investigate`, `/design-review`, `/devex-review`
4. QA/security: `/qa`, `/qa-only`, `/cso`, `/benchmark`
5. ship: `/ship`, `/land-and-deploy`, `/canary`, `/document-release`
6. memory/ops: `/learn`, `/context-save`, `/context-restore`, `/retro`, `/health`

In Hermes, load the closest generated skill before applying a gstack workflow. In the normalized `gstack-workflow` taxonomy, use the unprefixed skill names: for browser QA load `qa` or `browse`; for release flow load `ship`; for strategic product interrogation load `office-hours`. Treat old `gstack-*` prefixed directories as stale duplicates and archive them if they reappear.

## Browser automation quick reference

Use `gstack-browse` for fast Chromium automation when the gstack workflow calls for `$B` or browse commands.

```bash
gstack-browse goto https://example.com
gstack-browse snapshot -a
gstack-browse text
gstack-browse click @e3
gstack-browse fill 'input[name=email]' 'me@example.com'
gstack-browse console --errors
gstack-browse network
gstack-browse screenshot --viewport /tmp/page.png
gstack-browse pdf /tmp/page.pdf
gstack-browse tabs
gstack-browse stop
```

After `snapshot`, refs like `@e1`, `@e2`, `@c1` can be used as selectors.

Prefer native Hermes `browser_*` tools for simple browser tasks already supported in-session. Prefer `gstack-browse` when a gstack skill explicitly expects it, when you need the gstack daemon/session behavior, or when reproducing gstack workflows.

## Installation / update procedure

Safe reinstall/update:

```bash
mkdir -p ~/.claude/skills
if [ -d ~/.claude/skills/gstack/.git ]; then
  cd ~/.claude/skills/gstack
  git fetch --depth 1 origin main
  git reset --hard origin/main
else
  rm -rf ~/.claude/skills/gstack
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
fi
cd ~/.claude/skills/gstack
./setup --host claude --no-prefix --quiet
```

If setup times out during browser download, continue with:

```bash
cd ~/.claude/skills/gstack
bunx playwright install chromium
./setup --host claude --no-prefix --quiet
```

Then mirror Hermes generated skills if needed. Normalize generated directories from `gstack-<name>` to active Hermes skill folders named `<name>` so the profile ends with exactly 45 active `gstack-workflow` skills and no duplicate frontmatter names:

```bash
src="$HOME/.claude/skills/gstack/.hermes/skills"
dst="$HERMES_HOME/skills/gstack-workflow"
mkdir -p "$dst"
for d in "$src"/gstack*/; do
  [ -f "$d/SKILL.md" ] || continue
  raw=$(basename "$d")
  name="${raw#gstack-}"
  [ "$raw" = "gstack" ] && name="gstack"
  rm -rf "$dst/$name"
  mkdir -p "$dst/$name"
  ln -snf "$d/SKILL.md" "$dst/$name/SKILL.md"
done
# Sanity: should print 45.
find "$dst" -maxdepth 2 -name SKILL.md | wc -l
```

## Verification

Before claiming setup is done, verify:

```bash
cd ~/.claude/skills/gstack
git rev-parse --short HEAD
bun pm pkg get name version
bun --version
command -v gstack-browse
gstack-browse --help
bun --eval 'import { chromium } from "playwright"; const b = await chromium.launch({headless:true}); await b.close(); console.log("chromium ok")'
find ~/.claude/skills -maxdepth 2 -name SKILL.md | wc -l
find ~/.hermes/skills/gstack-workflow -maxdepth 3 -name SKILL.md | wc -l
```

## Profile isolation

For the Galyarder Hermes profile, gstack may intentionally exist alongside Keiya/default. If the user asks whether gstack is "double", answer the tool-path question directly first, then repair mixed wiring if needed. See `references/galyarder-profile-isolation.md` for the known-good path map, wrapper, verification commands, and cleanup pitfall. See `references/final-gstack-gbrain-routing-2026-05-12.md` for the final post-cleanup decision: two gstack repos are allowed for isolation, but each profile should keep exactly 45 active normalized `gstack-workflow` skill dirs; GBrain uses one canonical OS-home instance plus the thin Hermes `gbrain` skill.

## gstack vs gbrain vs Hermes cron

Do not conflate the three:

- **Hermes cron** schedules recurring assistant actions.
- **gstack** is the software-factory workflow suite: QA, review, ship/deploy, canary, browser testing, design/CEO/eng reviews.
- **gbrain** is a DB-backed personal/project brain with markdown import, embeddings, search/query, minions, and its own skillpack ecosystem.

If Galih asks "itu gstack ya? kalo gbrain gimana?", load `gbrain` and verify the actual GBrain CLI/repo/data/DB paths. In the Galyarder profile, `~/gbrain` may point to a profile-local install while the healthy canonical GBrain may be `/home/galyarder/gbrain`. Use the `gbrain` Hermes skill and see `gbrain/references/gbrain-profile-dedupe-2026-05-12.md`.

## Pitfalls

- gstack setup can take a long time because it installs packages, builds Bun binaries, generates host skills, and downloads Playwright Chromium/headless shell.
- The setup script has a special `--host hermes` branch that prints outlines and exits; it does not install into Hermes by itself. Generate/mirror `.hermes/skills` from the repo for Hermes use.
- Avoid loading many generated gstack skills at once; they are large. Load only the needed specialist skill.
- gstack uses generated `SKILL.md` files. In the gstack repo, edit templates/source config rather than generated files if contributing upstream.
- Browser automation may leave a daemon/session running; use `gstack-browse stop` when done. If it fails while processes remain, narrow cleanup to profile-local gstack paths; see the isolation reference.
