# Galyarder profile isolation for gstack

Use this when gstack appears "double" with Keiya/default, or when `gstack-browse` resolves to the OS-home wrapper while the active Hermes profile is `galyarder`.

## Expected two-workspace shape

Default/Keiya side:

```text
/home/galyarder/.claude/skills/gstack
/home/galyarder/.hermes/skills/gstack-workflow
/home/galyarder/.hermes/skills/devops/gstack-local
/home/galyarder/.local/bin/gstack-browse
/home/galyarder/.cache/ms-playwright
```

Galyarder profile side:

```text
/home/galyarder/.hermes/profiles/galyarder/home/gstack
/home/galyarder/.hermes/profiles/galyarder/home/.claude/skills/gstack
/home/galyarder/.hermes/profiles/galyarder/skills/gstack-workflow
/home/galyarder/.hermes/profiles/galyarder/skills/devops/gstack-local
/home/galyarder/.hermes/profiles/galyarder/home/.local/bin/gstack-browse
/home/galyarder/.hermes/profiles/galyarder/home/.cache/ms-playwright
```

Having two gstack repos is intentional if Keiya/default and Galyarder need isolated tooling state. The bug is not repo duplication; the bug is mixed wiring or duplicate generated Hermes skill directories. Keep exactly 45 active `gstack-workflow` skill dirs per profile.

## Repair wiring

```bash
PROFILE_HOME=/home/galyarder/.hermes/profiles/galyarder/home
PROFILE_SKILLS=/home/galyarder/.hermes/profiles/galyarder/skills

rm -rf "$PROFILE_SKILLS/gstack-workflow"
cp -a /home/galyarder/.hermes/skills/gstack-workflow "$PROFILE_SKILLS/gstack-workflow"

mkdir -p "$PROFILE_SKILLS/devops"
rm -rf "$PROFILE_SKILLS/devops/gstack-local"
cp -a /home/galyarder/.hermes/skills/devops/gstack-local "$PROFILE_SKILLS/devops/gstack-local"

mkdir -p "$PROFILE_HOME/.local/bin"
cat > "$PROFILE_HOME/.local/bin/gstack-browse" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
export HOME="/home/galyarder/.hermes/profiles/galyarder/home"
export GSTACK_HOME="$HOME/gstack"
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
exec "$HOME/.claude/skills/gstack/browse/dist/browse" "$@"
SH
chmod +x "$PROFILE_HOME/.local/bin/gstack-browse"
```

## Verification

```bash
PROFILE_HOME=/home/galyarder/.hermes/profiles/galyarder/home
B="$PROFILE_HOME/.local/bin/gstack-browse"

git -C "$PROFILE_HOME/gstack" rev-parse --short HEAD
bun --version
skill_view gstack-local      # or use the Hermes tool
skill_view gstack-browse     # or use the Hermes tool
"$B" --help
"$B" status
"$B" goto https://example.com
"$B" text
```

Known-good smoke result:

```text
repo commit: bf65487
bun: 1.3.11
browse status: Status: healthy
example.com goto: Navigated ... (200)
text includes: Example Domain
```

## Cleanup pitfall

`gstack-browse stop` can return `Unable to connect` while a profile-local browse daemon is still alive. If the user approves cleanup, target only profile-local gstack processes:

```bash
PROFILE_HOME=/home/galyarder/.hermes/profiles/galyarder/home
pgrep -af "$PROFILE_HOME/gstack/browse/src/server.ts|$PROFILE_HOME/.cache/ms-playwright/chromium_headless_shell"
# after approval:
pgrep -f "$PROFILE_HOME/gstack/browse/src/server.ts|$PROFILE_HOME/.cache/ms-playwright/chromium_headless_shell" | xargs -r kill
```

Do not kill broad `chromium` or `bun` processes without narrowing to the profile paths.

## Communication note

When the user asks whether a tool is "double", answer the direct tool question first: yes/no, which paths, and whether duplication is intentional. Do not detour into persona identity unless the user asked about identity.
