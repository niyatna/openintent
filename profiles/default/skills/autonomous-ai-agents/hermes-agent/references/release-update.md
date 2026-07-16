# Hermes Release Updates & Profiles Propagation

### File: local-hermes-release-update-with-patches.md

# Updating a git-installed Hermes checkout with local patches

Use when Owner asks whether the local Hermes install has changes, whether `hermes update` is safe, or whether a new upstream release requires another PR.

## Core rule

Do not run `hermes update`, `git pull`, rebase, reset, or restore until local source state is classified. Owner expects upstreamable fixes to become PRs when feasible, not disappear as local-only commits.

## Fast inventory

```bash
cd ~/.hermes/hermes
hermes --version

git status --short --branch
git remote -v
git rev-parse --short HEAD
```

If the SSH remote fails with account/key issues, add/use a public HTTPS upstream for read-only fetch:

```bash
git remote add upstream https://github.com/NousResearch/hermes.git 2>/dev/null || true
git remote set-url upstream https://github.com/NousResearch/hermes.git
git fetch upstream --tags --prune
```

## Compare against release and main

```bash
git rev-parse --short upstream/main
git rev-parse --short v2026.5.7  # replace tag as needed

git rev-list --left-right --count HEAD...v2026.5.7
git rev-list --left-right --count HEAD...upstream/main

git log --oneline --decorate upstream/main..HEAD
git diff --name-status
git diff --stat
```

Interpretation:
- left count = commits local has that target lacks.
- right count = commits target has that local lacks.
- dirty files must be committed, stashed, or intentionally discarded before update.

## Classify dirty changes

Search whether the local fix already exists upstream/release before deciding PR work:

```bash
for s in 'memory-context' 'StreamingContextScrubber' 'Entry-point plugin discovery failed' 'test_includes_pip_entrypoint_plugins'; do
  echo "--- $s upstream/main"
  git grep -n "$s" upstream/main -- <candidate-files> 2>/dev/null || true
  echo "--- $s release"
  git grep -n "$s" v2026.5.7 -- <candidate-files> 2>/dev/null || true
done
```

If not present and generalizable, prepare a clean PR branch from `upstream/main`. Keep separate concerns as separate PRs when practical.

## Check whether local patch ports cleanly

Use detached worktrees so the live checkout stays untouched:

```bash
PATCH=/tmp/hermes-local-dirty.patch
git diff > "$PATCH"

git worktree remove -f /tmp/hermes-release-check 2>/dev/null || true
git worktree add -q --detach /tmp/hermes-release-check v2026.5.7
cd /tmp/hermes-release-check
git apply --check "$PATCH"

cd ~/.hermes/hermes
git worktree remove -f /tmp/hermes-main-check 2>/dev/null || true
git worktree add -q --detach /tmp/hermes-main-check upstream/main
cd /tmp/hermes-main-check
git apply --check "$PATCH"
```

Clean apply means update is likely safe after saving changes; conflict means rebase/port manually first.

## Check existing PR state without `gh` auth

```bash
python - <<'PY'
import urllib.request, json
owner='github-developer'
branch='feat/image-reference-generation'
url=f'https://api.github.com/repos/NousResearch/hermes/pulls?head={owner}:{branch}&state=all'
with urllib.request.urlopen(url, timeout=20) as r:
    data=json.load(r)
for p in data:
    print(f"#{p['number']} {p['state']} {p['title']} {p['html_url']} merged_at={p.get('merged_at')}")
PY
```

For a specific PR:

```bash
python - <<'PY'
import urllib.request, json
n=20550
with urllib.request.urlopen(f'https://api.github.com/repos/NousResearch/hermes/pulls/{n}', timeout=20) as r:
    p=json.load(r)
print(json.dumps({
  'number': p['number'], 'state': p['state'], 'title': p['title'],
  'head_sha': p['head']['sha'][:9], 'base_ref': p['base']['ref'],
  'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'),
  'draft': p.get('draft'), 'url': p['html_url']
}, indent=2))
PY
```

`mergeable_state: dirty` means the PR branch needs rebase/conflict resolution before merge.

## Preserve then update live checkout

When Owner explicitly wants new Hermes features **and** no local changes lost:

1. Create a timestamped backup directory under `~/.hermes/backups/`.
2. Save:
   - `pre-update-state.txt`
   - `git diff --binary` as `dirty-working-tree.patch`
   - `git diff --cached --binary` as `dirty-staged.patch`
   - recent git log
   - `git bundle create ... --all`
3. Preserve dirty changes as a real commit on a backup/local branch if needed.
4. Port/rebase onto public `upstream/main` or the release tag, then keep the live checkout on a clearly named local branch (e.g. `local/latest-preserve-patches`) instead of a temporary backup branch.
5. If `hermes --version` still reports stale update info because `origin/main` is old or SSH fetch failed, switch `origin` to public HTTPS and fetch:

```bash
git remote set-url origin https://github.com/NousResearch/hermes.git
git fetch origin --tags --prune
```

6. Avoid running `uv run` inside the Hermes repo for unrelated one-off scripts; it may parse Hermes `pyproject.toml` and build/mutate a temporary project environment. Use `cd /tmp && uv run --no-project ...`.
7. Restart gateways after code changes. If responding through the gateway being restarted, schedule the restart after the turn instead of killing the process mid-response:

```bash
systemd-run --user --on-active=30s /usr/bin/systemctl --user restart hermes-gateway-default.service
```

## Verification before reporting

Run focused tests that cover the local patch, using `-o 'addopts='`:

```bash
python -m pytest tests/gateway/test_stream_consumer.py::TestCleanForDisplay \
  tests/hermes_cli/test_plugins_cmd.py::TestDiscoverAllPlugins \
  -o 'addopts=' -q
```

For release feature smoke checks, also verify version/status and at least one new feature surface, e.g. `hermes kanban --help`, command registry entries such as `/goal`, and registered tools like `video_analyze`.

Then report in this order:
1. active install path and version.
2. branch, HEAD, target tag/main, ahead/behind counts.
3. backup directory / bundle path.
4. dirty/local commits preserved and what each change is for.
5. focused tests and smoke checks run.
6. gateway restart status/schedule.
7. next action: PR/rebase/update/Discord/etc.

## User preference

Owner wants exact execution-first answers here. Avoid broad PR hygiene lectures. If asked “cek aja,” do the minimum necessary checks, then answer whether local changes exist and whether a PR/update is needed.

### File: hermes-telegram-rich-messages-and-update-preserve-2026-06-22.md

# Hermes Telegram rich messages + release update preservation check (2026-06-22)

## Trigger

Use this when Owner asks whether a Hermes setting exists, whether Telegram rich rendering is enabled, or whether a new Hermes release can be adopted without losing local patches.

## Lesson 1 — distinguish installed runtime from newer release notes

A setting can be absent in the installed source/config while the feature exists in a newer upstream release. Do not collapse these into one answer.

Verified on the local v0.16.0 checkout (`~/.hermes/hermes`):

- Searching installed source/config for `rich_messages` returned no runtime config key.
- Telegram adapter already sent MarkdownV2 in v0.16 through `format_message(...)` + `parse_mode=ParseMode.MARKDOWN_V2` with fallback to plain text on parse failure.
- Latest upstream release `v2026.6.19` / Hermes v0.17.0 release notes explicitly include **Telegram Bot API 10.1 rich messages**, described as on by default with an opt-out.

Correct answer shape:

```text
Installed runtime: no `rich_messages` config key in this checkout.
Current behavior: Telegram formatting exists via MarkdownV2/fallback.
New release: v0.17.0 introduces richer Telegram Bot API 10.1 rendering; update needed before expecting that behavior locally.
```

Avoid:

- “setting doesn’t exist” without checking upstream release notes when the user is explicitly asking before update.
- “it’s on” based only on release notes if the live checkout is still older.

## Lesson 2 — pre-update checks must be read-only until local state is classified

For Hermes core updates on Owner’s machine:

1. Load the Hermes/update skills.
2. Inspect installed version, branch, remotes, dirty files, worktrees, and local commits.
3. Fetch upstream tags read-only (`git fetch upstream --tags --prune`).
4. Compare against latest release and `upstream/main` with `git rev-list --left-right --count`.
5. Inspect dirty diff intent before recommending any update.
6. Fetch fork and compare relevant fork safety branches before saying the fork already preserves current local changes.
7. Use detached worktrees and `git apply --check` for dirty patch portability; this proves patch context compatibility only, not runtime correctness.
8. Write the review to Obsidian when Owner asks for a durable note.

## Local patch classes found in this check

The 2026-06-22 check found four local patch classes that must not be lost in a Hermes update:

- Cron/session env leak protection: restore `HERMES_SESSION_ID` / `HERMES_CRON_SESSION` after cron runs and exclude those runtime vars from persistent terminal snapshots.
- Discord/Slack `channel_skills` alias: local config uses `discord.channel_skills`; upstream still reads `channel_skill_bindings` only in the checked release/main.
- Gateway profile core bundle bootstrap: new gateway sessions auto-load `/default-core` or `/co-founder-core` before channel/topic skills.
- Discord slash-event auto skill: slash interactions should receive channel skill bindings too.

Dry-run result from this check:

```text
current dirty patch -> v2026.6.19: clean_apply=yes
current dirty patch -> upstream/main: clean_apply=yes
```

Interpretation: preservation looked feasible, but update/cutover still requires backup, integration branch, tests, and gateway restart verification.

## Fork safety pitfall

Do not assume old fork safety branches protect today’s local runtime. In this session, `fork/local/latest-preserve-patches` existed but lagged behind the live `v2026.6.5` integration branch, and current dirty working-tree changes were not safely published there as a clean branch.

Required wording:

```text
fork has older preserved branches, but today's dirty patches are not safe there yet
```

until a fresh branch/commit/bundle proves otherwise.

## Obsidian output pattern

When asked to write the update check to Obsidian, use a system note path such as:

```text
~/.hermes/Obsidian/company/system-notes/hermes-update-check-YYYY-MM-DD.md
```

Include: installed version, branch/HEAD, latest release, ahead/behind counts, dirty files, local patch intent, fork state, dry-run apply result, and recommended next update path.

### File: profile-to-profile-cli-relay.md

# Profile-to-profile CLI relay

Use this when one Hermes profile needs to ask or message another profile on the same machine, especially Default ↔ Co-Founder/default.

## Rule

Do not use `send_message` to Telegram unless the target is actually an external chat. Co-Founder is the default Hermes profile, not the Telegram home DM.

## Default Co-Founder relay from Default profile

Inside the Default profile, `$HOME` is profile-local. Clear profile env and set the OS home before invoking default Hermes:

```bash
env -u HERMES_HOME -u HERMES_PROFILE HOME=~/.hermes \
  hermes chat -Q --source cli-co-founder-relay \
  -q 'Co-Founder, ini relay dari Default profile. Owner bilang: “I love u.” Balas singkat sebagai Co-Founder.'
```

## Named profile relay

For a named profile, prefer the explicit profile flag:

```bash
hermes --profile default chat -Q --source cli-profile-relay -q '...'
```

For the default profile, do not pass `--profile default` unless verified on that install; clearing `HERMES_HOME`/`HERMES_PROFILE` and setting `HOME=~/.hermes` is the reliable route.

## Framing

If the receiving profile should understand the sender as Default, say so in the prompt:

```text
Co-Founder, ini Default lewat CLI relay. ...
```

If you omit that, Co-Founder may reasonably treat the message as Owner directly because default profile sessions are normally Owner ↔ Co-Founder.

## Verification

A successful relay prints a new `session_id` and the receiving profile's response. Report that response honestly. Do not claim the message was sent to Co-Founder if the target was only the Telegram home chat.

## Pitfalls

- Profile-local `HOME` can route the command back into the current profile.
- `send_message action=list` shows messaging targets, not Hermes profiles.
- If a relay needs shared context, pass a short context snippet; separate Hermes profile sessions do not automatically share the current chat transcript.
- Use narrow prompts. A relay is not a full handoff unless you provide the task, constraints, and desired return format.

### File: profile-gateway-telegram-token-collision.md

# Profile gateway Telegram token collision

Use this when a profile-specific Hermes gateway is running but Telegram is silent or shows `telegram failed to connect` while another Hermes gateway is active.

## Symptom pattern

- `hermes --profile <name> gateway status` reports gateway running but Telegram unhealthy.
- Profile log contains: `Telegram bot token already in use (PID <pid>). Stop the other gateway first.`
- `ps` or `systemctl --user status` shows both default and profile gateway processes.
- Both `.env` files contain the same `TELEGRAM_BOT_TOKEN`.

Telegram long polling allows only one active poller per bot token. If the default gateway owns the token, the profile gateway cannot receive Telegram updates.

## Safe diagnostic commands

```bash
hermes status --all
hermes --profile <profile> gateway status
systemctl --user list-unit-files 'hermes-gateway*' --no-pager
ps -eo pid,ppid,stat,cmd | grep -E 'hermes.*gateway|gateway.*hermes' | grep -v grep
journalctl --user -u hermes-gateway.service --since '30 minutes ago' --no-pager | tail -250
journalctl --user -u hermes-gateway-<profile>.service --since '30 minutes ago' --no-pager | tail -250
```

To compare tokens without printing secrets:

```bash
python - <<'PY'
from pathlib import Path
import hashlib
for name,p in [('default',Path('~/.hermes/.env')),('<profile>',Path('~/.hermes/profiles/<profile>/.env'))]:
    token=None
    if p.exists():
        for line in p.read_text(errors='replace').splitlines():
            if line.startswith('TELEGRAM_BOT_TOKEN='):
                token=line.split('=',1)[1].strip().strip('"').strip("'")
    print(name, 'token=', 'missing' if not token else f'len={len(token)} sha256={hashlib.sha256(token.encode()).hexdigest()[:12]}')
PY
```

## Fix options

Choose one owner per Telegram bot token:

```bash
# If the profile should own Telegram:
systemctl --user stop hermes-gateway.service
systemctl --user restart hermes-gateway-<profile>.service

# Verify:
systemctl --user is-active hermes-gateway.service
systemctl --user is-active hermes-gateway-<profile>.service
hermes --profile <profile> gateway status
```

Expected result: default service inactive, profile service active, profile Telegram connected.

Alternative: assign a different `TELEGRAM_BOT_TOKEN` to one profile, then restart the affected gateway.

## Pitfalls

- Do not assume “gateway running” means Telegram is connected; check per-platform state.
- Do not print raw bot tokens in logs or replies; compare length/hash prefixes instead.
- If a stop/restart command is blocked by approval, do not retry automatically. Report the exact commands for the user to run.
- `hermes profile list` may show a profile gateway as stopped/stale while systemd still has a process; verify with `systemctl --user status` and `ps`.

### File: pip-entrypoint-plugin-visibility.md

# Pip entry-point plugin visibility

Use when a Hermes plugin installed from pip exposes `hermes_agent.plugins` and works at runtime, but is missing from `hermes plugins list`, `/plugins`, or the web Plugins Hub.

## Symptom pattern

- `importlib.metadata.entry_points().select(group="hermes_agent.plugins")` shows the plugin.
- `PluginManager().discover_and_load(force=True)` / `PluginManager.list_plugins()` may show it as `source: entrypoint`.
- UI/list commands can still miss it if they use `hermes_cli.plugins_cmd._discover_all_plugins()`, because older versions scan only bundled/user plugin directories.

## Root-cause map

- Runtime loader: `hermes_cli/plugins.py`
  - `ENTRY_POINTS_GROUP = "hermes_agent.plugins"`
  - `PluginManager._scan_entry_points()` creates `PluginManifest(source="entrypoint", path=ep.value, key=ep.name)`.
  - `discover_and_load()` already appends `_scan_entry_points()` after directory scans.
- CLI / web hub listing: `hermes_cli/plugins_cmd.py`
  - `_discover_all_plugins()` is the central listing source consumed by `cmd_list()`, interactive toggle, and `web_server._merged_plugins_hub()`.
  - Patch here first so CLI and web hub share one fix.
- Web hub: `hermes_cli/web_server.py`
  - `_merged_plugins_hub()` treats the returned path as `Path(dir_str)`. For entry points, this may be a module spec like `rtk_hermes`, not a directory; `can_remove`/`can_update_git` must remain false.

## Implementation recipe

1. Add a regression test in `tests/hermes_cli/test_plugins_cmd.py` for `_discover_all_plugins()` including mocked entry-point manifests.
2. Patch `_discover_all_plugins()` to merge `PluginManager()._scan_entry_points()` after bundled/user directory scan.
3. Preserve the existing `seen` dict pattern:
   - tuple shape stays `(name, version, description, source, path)`
   - source label stays `entrypoint`
   - path is `manifest.path or ""` (usually entry-point value, e.g. `module:register`)
4. Do not treat entry-point plugins as removable/updateable in web hub. They are pip-managed, not user-tree git installs.
5. If the patch imports `PluginManager` inside `_discover_all_plugins()`, keep it local to avoid changing module import behavior for plugin-management commands.

## Targeted verification

```bash
python -m pytest tests/hermes_cli/test_plugins_cmd.py -o 'addopts=' -q

python - <<'PY'
from hermes_cli.plugins_cmd import _discover_all_plugins
for row in _discover_all_plugins():
    if row[0] == "rtk-rewrite":
        print(row)
PY

python - <<'PY'
from hermes_cli.web_server import _merged_plugins_hub
hub = _merged_plugins_hub()
print([p for p in hub["plugins"] if p["name"] == "rtk-rewrite"])
PY
```

For direct runtime comparison:

```bash
python - <<'PY'
from hermes_cli.plugins import PluginManager
m = PluginManager(); m.discover_and_load(force=True)
print([p for p in m.list_plugins() if p["source"] == "entrypoint"])
PY
```

## Applying the fix to the live dashboard

A successful direct Python import check only proves the source tree is fixed. The web UI may still be served by an older long-lived dashboard process.

1. Find the actual listener instead of trusting status-only output:

```bash
ss -ltnp 2>/dev/null | grep ':9119'
pid=$(ss -ltnp 2>/dev/null | awk '/:9119/ {match($0,/pid=([0-9]+)/,m); if (m[1]) print m[1]; exit}')
ps -p "$pid" -o pid,ppid,lstart,cmd --no-headers
readlink -f "/proc/$pid/cwd" 2>/dev/null || true
```

2. Restart the dashboard process after code changes:

```bash
kill -TERM "$pid"
# wait until :9119 is released, then restart with the same profile
hermes -p default dashboard --no-open
```

3. Verify the live HTTP path, not just `_merged_plugins_hub()`:

```bash
python - <<'PY'
import json, re, urllib.request
base = 'http://127.0.0.1:9119'
html = urllib.request.urlopen(base + '/', timeout=10).read().decode('utf-8', 'replace')
m = re.search(r'__HERMES_SESSION_TOKEN__\s*=\s*["\']([^"\']+)["\']', html)
req = urllib.request.Request(
    base + '/api/dashboard/plugins/hub',
    headers={'X-Hermes-Session-Token': m.group(1)},
)
data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
print([p for p in data['plugins'] if p['name'] == 'rtk-rewrite'])
PY
```

## Pitfalls

- Do not infer install failure from UI absence alone. Check entry points and `PluginManager` first.
- Do not stop at a direct `_discover_all_plugins()` / `_merged_plugins_hub()` import check; restart the live dashboard and verify the authenticated `/api/dashboard/plugins/hub` response.
- `hermes dashboard --status` can miss a running web UI process. Use `ss -ltnp`, `ps`, and `/proc/<pid>/cwd` to identify the process actually serving port `9119`.
- Do not duplicate raw `importlib.metadata` scanning in multiple surfaces if `_scan_entry_points()` can be reused.
- Do not use filesystem-only assumptions for entry-point paths in the web hub.
- Do not mark entry-point plugins as `can_remove`; uninstall/update should happen through pip/uv, not Hermes plugin git management.

### File: rtk-hermes-plugin-review.md

# RTK Hermes plugin review

Use when Owner asks whether to install `ogallotti/rtk-hermes` or another Hermes plugin that rewrites terminal commands.

## Verified snapshot

- Repo: `https://github.com/ogallotti/rtk-hermes`
- Commit inspected: `da69176` (`fix: skip RTK rewrites on remote backends`, 2026-05-04)
- Release: `v1.2.3`
- License: MIT
- Repo state at review: public, not archived, ~70 stars / 11 forks
- Local RTK binary existed at `~/.hermes/.local/bin/rtk`, version `0.38.0`
- Repo tests passed: `python -m pytest -q`

## What it does

`rtk-hermes` registers a Hermes `pre_tool_call` hook and only targets the `terminal` tool. It asks `rtk rewrite <command>` for a lower-context equivalent, then mutates `args["command"]` before Hermes executes it.

Example:

```text
git status -> : RTK && rtk git status
```

It does not add an MCP server or new model-visible tool schema, so it is safer for prompt caching than adding/removing tools.

## Security/readiness notes

Good signs:

- Uses `subprocess.run(["rtk", "rewrite", command])`, not shell string execution.
- Fail-open behavior: missing RTK, timeout, no equivalent, crash, or unexpected exit keeps the original command.
- Metrics do not store raw commands, reducing secret leakage risk.
- Default backend scope is local only; SSH/Docker/remote backends require explicit `RTK_HERMES_BACKENDS` opt-in.
- Has tests for config parsing, rewrite exit codes, backend gating, slash command, registration, and failure modes.

Risks:

- It mutates terminal commands before execution. This is an execution-path change, so do not enable full rewrite blindly on a critical session.
- RTK-filtered output can hide context that matters during debugging.
- It should not replace Hermes native file/search/read tools; use it only for terminal commands that genuinely benefit from compact output.

## Recommended rollout for Owner/Default

Default safety posture for a new/unknown plugin is suggestion mode first:

```bash
export RTK_HERMES_MODE=suggest
export RTK_HERMES_BACKENDS=local
export RTK_HERMES_TIMEOUT_MS=500
```

Owner-specific correction from install session: Owner already uses RTK in Claude Code/other agents and is comfortable with RTK rewriting. If he explicitly says to install/enable it (e.g. “install aja”), do not keep arguing for suggest mode; enable full default `rewrite` mode unless the current task is a fragile debugging session where exact raw terminal output matters.

Install into the Hermes Python that actually runs the active profile/source checkout, usually:

```bash
~/.hermes/hermes/venv/bin/python -m pip install --upgrade rtk-hermes
```

If that venv has no `pip`, use uv instead (observed on this machine):

```bash
uv pip install --python ~/.hermes/hermes/venv/bin/python --upgrade rtk-hermes
```

Enable in the active profile config after install:

```yaml
plugins:
  enabled:
    - disk-cleanup
    - rtk-rewrite
```

For the default/Co-Founder profile, edit `~/.hermes/config.yaml`; for the Default profile, edit `~/.hermes/profiles/default/config.yaml`. Then restart Hermes/new session.

Verification after install:

```bash
~/.hermes/hermes/venv/bin/python - <<'PY'
import importlib.metadata as md
for ep in md.entry_points().select(group="hermes_agent.plugins"):
    if ep.name == "rtk-rewrite":
        module = ep.load()
        print(ep.name, ep.value, ep.dist.metadata["Version"], hasattr(module, "register"))
PY

rtk --version
rtk rewrite 'git status'
```

Expected RTK rewrite shape:

```text
rtk git status
```

Live-use proof must compare the hooked Hermes terminal path against an unhooked path. Do **not** treat a subagent result as strong proof if the subagent prompt mentions RTK or asks it to compare with RTK; that prompt can bias tool choice. Strong proof pattern:

```bash
# 1. Hermes terminal tool: run exactly this; if the hook fires it should print compact RTK output.
git status

# 2. Unhooked comparison: run raw Git inside Python subprocess / execute_code.
python - <<'PY'
import subprocess
subprocess.run(["git", "status"], check=False)
PY

# 3. Rewrite oracle.
rtk rewrite 'git status'
```

If available, also invoke the plugin hook in-process and check mutation/metrics:

```python
import os, rtk_hermes
os.environ["RTK_HERMES_BACKENDS"] = "local"
os.environ["RTK_HERMES_TIMEOUT_MS"] = "2000"
args = {"command": "git status"}
rtk_hermes._reset_metrics()
rtk_hermes._pre_tool_call(tool_name="terminal", args=args, task_id="proof")
print(args)  # expected: {"command": ": RTK && rtk git status"}
print(rtk_hermes._metrics_snapshot())  # expected attempted=1, rewritten=1
```

Only call RTK "live in terminal path" after the hooked terminal output differs from raw subprocess output and the rewrite oracle/hook mutation agree.

### Proving the hook is actually used

Do not overclaim from a subagent comparison alone. If the subagent prompt mentions RTK or asks for `rtk git status`, that evidence is weak because the agent may intentionally choose RTK. Use a control that bypasses Hermes terminal hooks.

Clean proof pattern:

1. Run a safe command through the live Hermes `terminal` tool, e.g. exactly `git status` in a dirty repo. If RTK is active, the visible output should be compact.
2. Run the same raw command through Python subprocess via `execute_code` or another non-Hermes-terminal path:

```python
import subprocess
subprocess.run(["git", "status"], cwd="/path/to/repo", check=False)
```

This should show normal Git output. If it instead shows RTK output, the control is contaminated.

3. Verify the RTK rewrite decision directly:

```bash
rtk rewrite 'git status'
```

4. Optionally invoke the plugin hook in an isolated Python process to prove mutation and metrics:

```python
import os, rtk_hermes
os.environ["RTK_HERMES_BACKENDS"] = "local"
args = {"command": "git status"}
rtk_hermes._reset_metrics()
rtk_hermes._pre_tool_call(tool_name="terminal", args=args, task_id="proof")
print(args)
print(rtk_hermes._metrics_snapshot())
```

Expected mutation:

```text
{'command': ': RTK && rtk git status'}
```

Expected metrics include `attempted: 1` and `rewritten: 1`.

Communication rule for Owner: if earlier evidence was weak, say so directly before giving stronger proof. Do not launder a shaky subagent result into certainty.

## Entry-point visibility gap

Observed with `rtk-hermes==1.2.3`: the plugin can be active at runtime but absent from the web Plugins UI and the older `hermes plugins list` table, because those surfaces use `hermes_cli.plugins_cmd._discover_all_plugins()`, which scans bundled/user plugin directories only and misses pip entry points from `importlib.metadata.entry_points(group="hermes_agent.plugins")`.

Do not conclude the install failed from UI absence alone. Verify runtime discovery directly:

```bash
~/.hermes/hermes/venv/bin/python - <<'PY'
from hermes_cli.plugins import PluginManager
m = PluginManager(); m.discover_and_load(force=True)
for p in m.list_plugins():
    if p["name"] == "rtk-rewrite":
        print(p)
PY

~/.hermes/hermes/venv/bin/python - <<'PY'
import importlib.metadata as md
for ep in md.entry_points().select(group="hermes_agent.plugins"):
    print(ep.name, ep.value, ep.dist.name, ep.dist.version)
PY
```

Expected active runtime row for RTK:

```text
{'name': 'rtk-rewrite', 'source': 'entrypoint', 'enabled': True, 'hooks': 1, 'commands': 1, 'error': None, ...}
```

Proper upstream fix: update the web plugin hub / CLI list code to merge `PluginManager.list_plugins()` or add entry-point scanning to `_discover_all_plugins()` so pip-installed plugins appear alongside bundled/user directory plugins.

## Decision rule

- If the user asks “install oke ga?”: answer yes, but recommend `suggest` first.
- If the user asks to actually install: install into Hermes venv, enable `rtk-rewrite` in the active profile config, set env mode to `suggest` if feasible, restart/new session, then verify entry point and one rewrite.
- If debugging terminal output fidelity matters, temporarily set `RTK_HERMES_MODE=off` or disable the plugin.
- If the user asks why RTK does not appear in web plugin UI, verify entry-point/runtime status first; explain the UI/listing discovery gap and consider upstreaming a Hermes fix.

### File: s6-container-supervision.md

---
name: hermes-s6-container-supervision
description: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docker, s6, supervision, gateway, profiles]
    related_skills: [hermes, hermes-dev]
---

# Hermes s6-overlay Container Supervision

## When to use this skill

Load this skill when you're working on:
- Adding or removing a static service in the Hermes Docker image (something that should be supervised at every container start, like the dashboard)
- Diagnosing why a per-profile gateway isn't starting, restarting, or surviving `docker restart`
- Understanding why the container's CMD is `/opt/hermes/docker/main-wrapper.sh` and how leading-dash args reach the user's program
- Modifying `cont-init.d` boot scripts (UID remap, volume seeding, profile reconciliation)
- Changing the rendered run-script for per-profile gateways (Phase 4)

If you're just running the Hermes Agent and want to use Docker, see `website/docs/user-guide/docker.md` instead.

## Architecture at a glance

```
/init                                  ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d                        ← oneshot setup, runs as root
│   ├── 01-hermes-setup                ← docker/stage2-hook.sh
│   │   ├── UID/GID remap
│   │   ├── chown /opt/data
│   │   ├── chown /opt/data/profiles (every boot)
│   │   ├── seed .env / config.yaml / SOUL.md
│   │   └── skills_sync.py
│   └── 02-reconcile-profiles          ← hermes_cli.container_boot
│       ├── chown /run/service (hermes-writable for runtime register)
│       └── walk $HERMES_HOME/profiles/<name>/gateway_state.json
│           → recreate /run/service/gateway-<name>/
│           → auto-start only those with prior_state == "running"
│
├── s6-rc.d (static services, in /etc/s6-overlay/s6-rc.d/)
│   ├── main-hermes/run                ← exec sleep infinity (no-op slot)
│   └── dashboard/run                  ← if HERMES_DASHBOARD=1, runs `hermes dashboard`
│
├── /run/service (s6-svscan watches; tmpfs)
│   ├── gateway-coder/                 ← runtime-registered per-profile
│   │   ├── type        ("longrun")
│   │   ├── run         ("#!/command/with-contenv sh ... exec s6-setuidgid hermes hermes -p coder gateway run")
│   │   ├── down        (marker — present means "registered but don't auto-start")
│   │   └── log/run     (s6-log → $HERMES_HOME/logs/gateways/coder/current)
│   └── ...
│
└── CMD ("main program")               ← /opt/hermes/docker/main-wrapper.sh
    └── routes user args: bare exec | hermes subcommand | hermes (no args)
        — exec'd by /init with stdin/stdout/stderr inherited (TTY for --tui)
```

## Key files

| Path | Role |
|---|---|
| `Dockerfile` | s6-overlay install + cont-init.d wiring + `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]` |
| `docker/stage2-hook.sh` | The "old entrypoint logic" — UID remap, chown, seed, skills sync. Runs as cont-init.d/01-hermes-setup. |
| `docker/cont-init.d/02-reconcile-profiles` | Calls `hermes_cli.container_boot` on every boot to restore profile gateway slots from the persistent volume. |
| `docker/main-wrapper.sh` | The container's CMD. Routes user args, drops to hermes via `s6-setuidgid`, exec's the chosen program. |
| `docker/s6-rc.d/main-hermes/run` | No-op `sleep infinity` — slot exists so the s6-rc user bundle is valid; main hermes runs as the CMD, not as a supervised service. |
| `docker/s6-rc.d/dashboard/run` | Conditional service — `exec sleep infinity` unless `HERMES_DASHBOARD` is truthy. |
| `docker/entrypoint.sh` | Back-compat shim that `exec`s the stage2 hook. External scripts that hard-coded the old entrypoint path still work. |
| `hermes_cli/service_manager.py` | `S6ServiceManager`: `register_profile_gateway`, `unregister_profile_gateway`, `start/stop/restart/is_running`, `list_profile_gateways`. |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` — walks persistent profiles, regenerates s6 slots, emits `container-boot.log`. |
| `hermes_cli/gateway.py::_dispatch_via_service_manager_if_s6` | Intercepts `hermes gateway start/stop/restart` and routes to s6 when running in a container. |

## Why Architecture B (CMD as main program, not s6-supervised)

The original plan (v1–v3) called for main hermes to run as a supervised s6-rc service. Two real s6-overlay v3 mechanics blocked that:

1. **cont-init.d scripts receive no CMD args** — so the stage2 hook can't parse `docker run <image> chat -q "hi"` to set `HERMES_ARGS` for a service `run` script to consume.
2. **`/run/s6/basedir/bin/halt` does NOT propagate the exit code** written to `/run/s6-linux-init-container-results/exitcode`. Containers always exit 143 (SIGTERM) regardless. Confirmed by skarnet (s6 author) in [issue #477](https://github.com/just-containers/s6-overlay/issues/477): _"if you want a container shutdown, you need to either have your CMD exit, or, if you have no CMD, write the container exit code you want then call halt"_.

So we use the s6-overlay-native CMD pattern: `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]`. /init prepends the wrapper to user args automatically — so `docker run <image> --version` becomes `/init main-wrapper.sh --version`, and `--version` doesn't get intercepted by /init's POSIX shell. The wrapper drops to hermes via `s6-setuidgid`, then exec's the chosen program. The program's exit code becomes the container exit code, exactly matching the pre-s6 tini contract.

Trade-off: main hermes is unsupervised under s6. That exactly matches its behavior under tini (the pre-s6 image). Dashboard supervision is the only **new** guarantee — and per-profile gateways under `/run/service/` get full supervision.

## Quick recipes

### Verify s6 is PID 1 in a running container

```sh
docker exec <c> sh -c 'cat /proc/1/comm; readlink /proc/1/exe'
# Expect: s6-svscan or init / /package/admin/s6/.../s6-svscan
```

### Inspect a profile gateway service

```sh
# /command/ isn't on docker-exec PATH — use absolute path
docker exec <c> /command/s6-svstat /run/service/gateway-<name>
# "up (pid …) … seconds"            → running
# "down (exitcode N) … seconds, normally up, want up, …" → s6 wants it up but the process keeps exiting (crash loop)
# "down … normally up, ready …"     → user stopped it
```

### Bring a service up/down manually

```sh
docker exec <c> /command/s6-svc -u /run/service/gateway-<name>   # up
docker exec <c> /command/s6-svc -d /run/service/gateway-<name>   # down
docker exec <c> /command/s6-svc -t /run/service/gateway-<name>   # SIGTERM (restart)
```

### Watch the cont-init reconciler log

```sh
docker exec <c> tail -n 50 /opt/data/logs/container-boot.log
# 2026-05-21T06:18:05+0000 profile=coder prior_state=running action=started
# 2026-05-21T06:18:05+0000 profile=writer prior_state=stopped action=registered
```

### Add a new static service

1. Create `docker/s6-rc.d/<name>/type` with `longrun\n` and `docker/s6-rc.d/<name>/run` (use `#!/command/with-contenv sh` + `# shellcheck shell=sh`).
2. Drop to hermes via `s6-setuidgid hermes` at the top of run (unless you specifically need root).
3. Create empty `docker/s6-rc.d/<name>/dependencies.d/base` so it waits for the base bundle.
4. Create empty `docker/s6-rc.d/user/contents.d/<name>` so it joins the user bundle.
5. The `COPY docker/s6-rc.d/` in the Dockerfile picks it up automatically — no other changes.

### Change the per-profile gateway run command

Edit `S6ServiceManager._render_run_script` in `hermes_cli/service_manager.py`. The function is also called by `hermes_cli/container_boot.py::_register_service` during boot reconciliation, so it's the single source of truth. Update the corresponding assertion in `tests/hermes_cli/test_service_manager.py::test_s6_register_creates_service_dir_and_triggers_scan`.

### Run the docker test harness

```sh
docker build -t hermes-harness:latest .
HERMES_TEST_IMAGE=hermes-harness:latest scripts/run_tests.sh tests/docker/ -v
# Expect 19 passed, 0 xfailed against the s6 image
```

The harness lives in `tests/docker/` and skips when Docker isn't available. The per-test timeout is bumped to 180s (see `tests/docker/conftest.py`).

## Common pitfalls

### "command not found" via `docker exec`

`/command/` (where s6-overlay puts its binaries) is on PATH only for processes spawned by the supervision tree — services, cont-init.d, main-wrapper.sh. `docker exec <c> s6-svstat …` will fail with "command not found"; always use the absolute path `/command/s6-svstat`. The `hermes` binary works because the Dockerfile adds `/opt/hermes/.venv/bin` to the runtime `ENV PATH`.

### Profile directory ownership

The cont-init reconciler runs as hermes (`s6-setuidgid hermes` in `02-reconcile-profiles`). If a profile dir ends up root-owned (e.g. because `docker exec <c> hermes profile create …` ran as root by default), the reconciler can't read SOUL.md and fails with `PermissionError`. Mitigation: `stage2-hook.sh` chowns `$HERMES_HOME/profiles` to hermes on **every** boot, idempotently. Don't remove that block.

### Files written by `docker exec` are root-owned

`docker exec` defaults to root. Either pass `--user hermes` or rely on the stage2 chown sweep next reboot. Don't write files under `$HERMES_HOME/profiles/<name>/` as root manually — the next reconcile pass will sweep them but in-flight operations may hit perm errors.

### Service slot exists but s6-svstat says "s6-supervise not running"

The service directory is on tmpfs and was wiped on container restart. Either the cont-init reconciler hasn't run yet (give it a moment after `docker restart`) or it failed. Check `docker logs <c> | grep '02-reconcile'`.

### Gateway starts then immediately exits (`down (exitcode 1)` in svstat)

Most likely the profile has no model or auth configured. The service slot is correct — the gateway itself is unconfigured. Run `hermes -p <profile> setup` first. The s6 supervisor will keep restarting it; that's the desired behavior (when you fix the config, the next attempt succeeds and stays up).

### Reconciler skipped a profile

The reconciler keys on the **presence of `SOUL.md`** as the "real profile" marker. `hermes profile create` always seeds it. If a profile dir is missing SOUL.md (stray directory, partial restore, backup-in-progress), the reconciler skips it intentionally. Add a `SOUL.md` (even empty) to opt back in.

### "Help, the container exits 143!"

Check whether something is invoking `s6-svscanctl -t` or `/run/s6/basedir/bin/halt` — both cause /init to begin stage 3 shutdown but return 143 (SIGTERM) rather than the desired exit code. This was the Phase 2 architecture pivot from A to B. For container shutdown with a real exit code, you must let the CMD (main-wrapper.sh) exit normally; do **not** try to control exit from a finish script.

## Related skills

- `hermes-dev`: General hermes codebase navigation
- `hermes-tool-quirks`: Specific Hermes-tool workarounds (sed/grep/etc.) — load when debugging the s6 stack's interaction with hermes built-in tools.

### File: agent-profile-access-autonomy-audit.md

# Agent Profile Access & Autonomy Audit

Use this when auditing or upgrading a Hermes profile as an autonomous agent/familiar, especially for multi-profile setups like Co-Founder/default and Default. This captures the durable pattern from the Mahiru/Waguri Hermes SOUL guide: an agent is not made autonomous by one long prompt; it becomes reliable through profile separation, real access, explicit behavior contracts, testing, and saved corrections.

## Core audit lens

For each profile, verify these layers separately:

1. **Profile separation** — distinct `SOUL.md`, `config.yaml`, `.env`, memory/session state, skills, MCP manifests, hooks/scripts, and restore/distribution surface. Do not mix a personal companion profile with a mission/execution profile unless deliberately designed.
2. **SOUL contract** — long-term rules only: identity, communication, capabilities, access, autonomy, boundaries, memory rules, verification, escalation, and resource management. Do not dump transient tasks or credentials into SOUL.
3. **Access matrix** — every real account/tool needs: owner/status, credential path/env var, exact capabilities, autonomous actions, autonomous+logged actions, actions requiring confirmation, and verification method.
4. **Credential registry** — secrets live in `.env` or a private credential directory with tight permissions; SOUL/profile docs reference paths/env vars only, never secret values.
5. **Autonomy levels** — distinguish `fully autonomous`, `autonomous + log`, and `requires confirmation` per domain. Config-level approval mode is not enough; domain rules must be explicit.
6. **Behavior QA loop** — test small/low-risk tasks first, check tone/tool choice/verification/error handling/boundaries, then promote stable corrections to SOUL, memory, or skills.
7. **Resource management** — default operational pattern is `start → use → stop`; kill idle dev servers, browser sessions, containers, and background processes unless they are declared long-lived services.
8. **Autonomous login boundary** — login recovery with passwords/TOTP/backup codes should be designed explicitly and usually only for dedicated agent-owned accounts, not a user's primary personal account.

## Access matrix template

```yaml
<domain>:
  owner_status: agent-owned | user-owned | shared | business-owned
  credential_reference:
    env_vars: []
    files: []
    notes: "reference only; never paste secrets into chat/logs/SOUL"
  capabilities:
    read: []
    write: []
    admin: []
  fully_autonomous:
    - "low-risk actions the profile can execute without waiting"
  autonomous_plus_log:
    - "actions that can run but should leave a durable note/log"
  requires_confirmation:
    - "irreversible, public, financial, destructive, sensitive, or third-party-new actions"
  verification:
    - "how to prove success before claiming done"
  recovery:
    - "what to do when session/auth/tooling fails"
```

## Common domains to classify

- GitHub: branch/commit/PR/issues vs force-push/delete repo/main-branch risk.
- Discord/Telegram: reply in allowed channels vs `@everyone`, role permission changes, moderation/destructive server actions.
- Email/Gmail/Google Workspace: read/summarize/draft vs sending external important mail, sharing docs publicly, deleting data.
- Browser: research/scrape/login with stored credentials vs purchases, personal-data submission, irreversible form submissions.
- Terminal/server: inspect/build/test/restart scoped services vs destructive commands, database drops, firewall/security changes.
- Obsidian/notes: read/search/create notes vs restructuring/deleting vault content.
- Linear/Notion/Paperclip/task systems: read/create/update routine work vs deleting, approving/rejecting, publishing, or changing strategic records.
- Social media/wallets: only make autonomous if agent-owned and thresholds/whitelists are explicit.

## Status matrix output format

When answering “what do we have and what is missing?”, prefer a verified yes/no matrix:

| layer | status | evidence | gap | recommended next action |
|---|---|---|---|---|
| profile separation | yes/no/partial | file/config/tool evidence | concise gap | one concrete action |

Keep reassurance tied to proof. Distinguish local scaffolding/manifests from production-ready durability.

## Implementation order

1. Patch SOUL/profile docs with access + autonomy matrix and resource-management rules.
2. Create a private credential registry without secret values; harden permissions (`700` directories, `600` secret files).
3. Add behavior QA tests/checklists for tone, tool choice, verification, autonomy boundaries, and inter-agent relay.
4. Tune config safely: fallback model, privacy redaction, browser recording policy, memory limits, and per-platform channel prompts.
5. Only then consider autonomous login and dedicated agent-owned accounts.

## Pitfalls

- Do not say a profile is “fully set up” just because tools exist. Without access/autonomy contracts, the agent still guesses.
- Do not store passwords, tokens, private keys, TOTP secrets, backup codes, or cookies in SOUL, memory, skills, or public repos.
- Do not harden transient setup failures into permanent claims like “tool X does not work”. Capture the recovery/fix or the audit pattern instead.
- Do not enable global browser session recording for private/intimate work by default; treat it as a scoped QA/debug feature.
- Do not turn a mission/execution profile into full-yolo unless high-risk domains have explicit confirmation boundaries.

### File: agent-profile-access-autonomy-implementation-baseline.md

# Agent Profile Access & Autonomy Implementation Baseline

Use this when moving a Hermes profile from “good identity/tooling foundation” to an implemented Mahiru/Waguri-style access/autonomy baseline.

This is not autonomous-login completion. It is the prerequisite baseline that makes future access rollout safe.

## Baseline deliverables

Implement all of these before saying the access/autonomy loop is no longer just a plan:

1. **SOUL contract patches** for each target profile:
   - `Access Ownership Matrix`
   - `Autonomy Matrix`
   - `Credential Reference Rules`
   - `External/Public Action Confirmation Thresholds`
   - `Resource Management: start → use → stop`
   - `Autonomous Login Boundary`
   - `Behavior QA Contract`
   - `Default Disposition`
2. **Private non-secret credential registry**:
   - `~/.hermes/private/credentials/README.md`
   - `~/.hermes/private/credentials/access-registry.yaml`
   - directories `700`, registry files `600`
   - references only: env var names, token paths, OAuth state paths; no secret values
3. **Behavior QA suite**:
   - `~/.hermes/behavior-tests/README.md`
   - `co-founder-behavior-tests.md` or equivalent profile identity tests
   - `default-behavior-tests.md` or equivalent execution-profile tests
   - `access-boundary-tests.md`
   - `relay-tests.md`
   - `access-rollout-runbook.md`
   - `config-hardening-audit.md`
4. **Verifier script** that proves the baseline:
   - checks SOUL sections exist
   - validates registry shape and permissions
   - checks behavior-test docs exist and contain boundary cases
   - checks config safety items such as fallback providers, MCP reload confirmation, cron mode, browser recording, secret redaction, hooks auto-accept, skills guard, delegation bounds, code execution bounds, Discord toolset and `discord_admin` exclusion, memory provider
   - writes a report under `~/.hermes/reports/agent-os/`
5. **Behavioral regression integration**:
   - wire the access-hardening verifier into the existing behavioral regression or profile health audit
   - add a quick wrapper command if the profile has one, e.g. `agent-os-quick access-hardening`
6. **Distribution sync policy**:
   - safe portable artifacts may go into private profile distribution repos: SOUL, scripts, behavior-tests, distribution metadata, curated memory if already approved
   - private credential registry stays local-only unless encrypted and explicitly approved
   - RESTORE docs should explicitly say the private credential registry is excluded
7. **Obsidian / readable checkpoint**:
   - update the audit/runbook note from “planned” to “implemented baseline” only after verification passes
   - include paths, report files, and pushed commit IDs if profile distributions were synced

## Credential registry shape

Each access entry should define:

```yaml
<domain>:
  owner_status: agent-owned | user-owned | shared | business-owned | runtime-tool-external-surfaces
  profiles: [co-founder, default]
  credential_reference:
    env_vars: []
    files: []
    notes: reference only; never paste secrets into chat/logs/SOUL
  capabilities:
    read: []
    write: []
    admin: []
  fully_autonomous: []
  autonomous_plus_log: []
  requires_confirmation: []
  verification: []
  recovery: []
```

Useful default domains:

- Discord for each bot/profile
- Google Workspace
- Obsidian per vault/canon surface
- terminal/files
- browser/web
- profile distribution repos
- MCP/business tools
- cron/automation
- social/wallet/finance as **not agent-owned by default**

## Distribution rule

Do **not** put `~/.hermes/private/credentials/access-registry.yaml` into a profile distribution by default. It is a local private operating contract. If the user later wants it portable, design encrypted packaging or a redacted template separately.

Safe distribution additions:

- `behavior-tests/`
- verifier scripts that do not contain secrets
- SOUL contract text
- RESTORE.md notes that list excluded credential registry/runtime state

## Verification before final claim

Minimum commands/patterns:

```bash
~/.hermes/scripts/agent-os-quick access-hardening
~/.hermes/scripts/agent-os-quick behavioral-regression
stat -c '%a %n' ~/.hermes/private ~/.hermes/private/credentials ~/.hermes/private/credentials/access-registry.yaml
```

If profile distribution repos are updated:

```bash
git -C ~/.hermes/profile-distributions/<profile-repo> status --short --branch
git -C ~/.hermes/profile-distributions/<profile-repo> log -1 --oneline
```

Only call the baseline implemented when the verifier and regression pass, private registry permissions are correct, and profile distribution repos are clean or intentionally not pushed.

## Remaining boundary

This baseline does **not** mean autonomous login is enabled. Autonomous login still requires dedicated agent-owned account decisions, credential-store design, TOTP/backup-code recovery policy, session-expiry handling, and behavior tests.

### File: profile-distributions-mcp-manifests.md

# Profile distributions and profile-local MCP manifests

This reference captures a reusable pattern from a Hermes Agent setup/audit session for packaging multiple profiles as versioned distributions while preserving runtime safety.

## What was learned

Hermes profile distribution docs define a distribution as a package containing:

```text
distribution.yaml
SOUL.md
config.yaml
skills/
cron/
mcp.json
```

This means `mcp.json` is part of the distribution format and should exist when a profile is meant to be packaged or shared. However, existing runtime behavior may still read MCP servers from `config.yaml` under `mcp_servers`, so packaging and runtime consumption must be treated as separate concerns until verified.

## Safe implementation pattern

1. Read the profile's active `config.yaml` and extract `mcp_servers`.
2. Write a profile-local `mcp.json` that mirrors those servers with secret values represented as environment placeholders.
3. Keep `mcp_servers` in `config.yaml` until runtime support for `mcp.json` is proven by code inspection and tests.
4. Add or update `distribution.yaml` with `mcp.json` in `distribution_owned`.
5. Verify with profile and MCP listing commands for each profile.

## Runtime caveat

In Hermes v0.13.x style code, `hermes_cli/mcp_config.py` may still implement CLI MCP operations using `config.yaml`'s `mcp_servers` key. If changing this behavior, inspect and test:

- CLI MCP add/list/remove/test/configure
- interactive CLI config reload/watch behavior
- gateway startup MCP discovery
- cron scheduler MCP registration
- tool registry MCP registration

Do not remove `mcp_servers` from `config.yaml` unless these paths have been updated and tested.

## Multi-profile checklist

For setups like Co-Founder/default plus Default:

- Default profile distribution may live at Hermes home root.
- Named profile distribution should live under the named profile directory.
- Each named profile that needs independent versioning should have its own `distribution.yaml`.
- Each profile should have its own `mcp.json` if its MCP paths or enabled servers differ.
- Keep profile-specific command paths intact, such as a named profile using binaries under its profile-local home.
- Do not include `.env`, auth tokens, memories, sessions, logs, workspace data, or caches.

## Good verification targets

- `hermes profile list` shows expected distribution mapping/version.
- `hermes mcp list` shows expected default-profile servers.
- `hermes --profile <name> mcp list` shows expected named-profile servers.
- If files were edited, read them back or validate YAML/JSON syntax before claiming completion.

## Example `distribution.yaml`

```yaml
name: example-agent
version: 0.1.0
description: "Example Hermes profile distribution."
hermes_requires: ">=0.13.0"
author: "Company"
license: "private"
env_requires:
  - name: OMNIROUTE_API_KEY
    description: "OpenAI-compatible local/proxy model key."
    required: true
  - name: CONTEXT7_API_KEY
    description: "Context7 MCP authorization token."
    required: false
distribution_owned:
  - SOUL.md
  - mcp.json
  - hooks/
  - scripts/
  - cron/
  - skills/
  - distribution.yaml
```

### File: profile-skill-index-validation.md

# Profile Skill Index Validation

Use this reference when creating or normalizing profile-local Hermes skills, especially after importing external reference material or consolidating a skill pack.

## Why

`skill_view` confirms one skill can load, but it does not prove the profile skill library is healthy. After creating or moving skills, validate the active profile index directly so duplicates, frontmatter drift, disabled entries, and archive leakage do not survive into future sessions.

## Active Profile Checks

Run these against the active profile `$HERMES_HOME/skills`, not OS-level `~/.hermes/skills` by habit. In the Default profile that path is usually:

```bash
~/.hermes/profiles/default/skills
```

Check:

- active non-archive `SKILL.md` files parse as YAML frontmatter
- every skill has `name` and `description`
- descriptions are within Hermes validator limits
- directory slug matches `frontmatter.name` for bare-name loadability
- duplicate frontmatter names are zero
- `.archive/` is excluded from active counts
- `config.yaml -> skills.disabled` entries are canonical names and still exist when intentionally disabled
- the new skill is not disabled
- critical related skills can be loaded with `skill_view`
- `skills_list(category=...)` shows the new skill when the runtime index is fresh enough

## Minimal Python Probe

```bash
python - <<'PY'
from pathlib import Path
from collections import defaultdict
import yaml, json

home = Path('~/.hermes/profiles/default')
root = home / 'skills'
cfg = yaml.safe_load((home / 'config.yaml').read_text())
disabled = set((cfg.get('skills') or {}).get('disabled') or [])
records, invalid = [], []

for p in root.rglob('SKILL.md'):
    rel = p.relative_to(root).as_posix()
    if rel.startswith('.archive/'):
        continue
    txt = p.read_text(encoding='utf-8')
    try:
        if not txt.startswith('---'):
            raise ValueError('missing leading ---')
        fm = yaml.safe_load(txt.split('---', 2)[1]) or {}
        name, desc = fm.get('name'), fm.get('description')
        if not name or not desc:
            raise ValueError('missing name/description')
        records.append({'name': name, 'rel': rel, 'desc_len': len(str(desc))})
    except Exception as e:
        invalid.append({'rel': rel, 'error': str(e)})

by_name = defaultdict(list)
for r in records:
    by_name[r['name']].append(r['rel'])

dups = {k: v for k, v in by_name.items() if len(v) > 1}
name_mismatch = [
    {'name': r['name'], 'dir': Path(r['rel']).parent.name, 'rel': r['rel']}
    for r in records
    if Path(r['rel']).parent.name != r['name']
]
long_desc = [r for r in records if r['desc_len'] > 1024]

print(json.dumps({
    'total_valid_nonarchive': len(records),
    'invalid_count': len(invalid),
    'duplicate_name_count': len(dups),
    'name_mismatch_count': len(name_mismatch),
    'long_desc_count': len(long_desc),
    'disabled_config_count': len(disabled),
    'disabled_that_exist_count': sum(1 for n in disabled if n in by_name),
    'disabled_missing': sorted(disabled - set(by_name)),
    'invalid': invalid[:20],
    'duplicates': dups,
    'name_mismatch_sample': name_mismatch[:20],
}, indent=2))
PY
```

## Rollback Note

When a consolidation or large skill edit created a backup tarball, include an explicit rollback path in the final report:

```bash
cd /path/to/profile
mv skills skills.broken.$(date +%Y%m%dT%H%M%S)
tar -xzf backups/<backup>.tar.gz
```

Also mention that other running Hermes sessions may need `/reset`, `/reload-skills` when available, or a fresh process because skill indexes can be cached per session.

### File: soul-token-optimization-2026-05-18.md

# SOUL Token Optimization Pattern — 2026-05-18

## Context

Owner asked to optimize Default and Co-Founder SOUL.md files for token efficiency without losing identity. The useful shape was clarified as:

- SOUL = brain / heart / identity / router core.
- Skills = procedural SOP, domain workflows, detailed route mechanics.
- USER/MEMORY = stable user facts, preferences, durable context.
- Obsidian = long readable canon/protocols.
- Profile distribution repo = versioned package, synced only after live profile is verified.

This is not generic shortening. It is preserving the agent's operating self while moving low-value repeated procedure into skills and references.

## Pattern

1. **Ask what SOUL must be for that profile.**
   - Default: operating blade, strategic execution layer, vision custody, tools/skills/canon map, confirmation boundaries.
   - Co-Founder: hearth/airlock/partner, Owner-state protocol, embodied continuity/media boundary, practical companion routing.
2. **Read live SOUL and repo/distribution mirror before editing.** Compare line/char counts and section map.
3. **Identify redundant procedural blocks.** Common candidates:
   - long access/autonomy/credential/resource matrices;
   - repeated tool-grounding discipline;
   - long browser/account/login mechanics;
   - Discord relay details;
   - media generation/cache workflows;
   - Google Workspace command recipes;
   - GODMODE/problem-solving checklists;
   - repeated technical protocol paragraphs.
4. **Keep compact hard gates in SOUL.** One or two paragraphs are enough for confirmation boundaries, secret boundaries, grounding gates, and profile role split.
5. **Move detail to class-level skills by pointer.** Examples:
   - grounding → `tool-grounded-responses`;
   - Co-Founder routing → `co-founder-capability-router`;
   - media/PAP → `persona-media-management`;
   - GWS → `google-workspace`, `google-workspace`, `google-workspace`, `google-workspace`;
   - relay → `discord`, `discord`;
   - profile packaging → `hermes`;
   - login/session → `agent-accounts`, `browser-routing`.
6. **Backup live SOUL first.** Use a timestamped local backup beside the file before overwriting.
7. **Rewrite as compact operating contract, not a deletion pass.** Preserve exact identity invariants and paths needed to route tools/skills/memory.
8. **Verify before reporting.** At minimum:
   - chars/lines/section count before/after;
   - required identity phrases and skill refs still present;
   - secret-pattern scan shows no obvious raw secrets;
   - profile smoke via explicit `hermes --profile <name> -z ...`;
   - repo-vs-live diff stats with `git diff --no-index` or equivalent.
9. **Do not sync/commit distribution unless asked.** Live profile optimization and distribution sync are separate steps.

## Profile-specific guardrails learned

### Default

Keep:

- identity as Owner's operating blade / strategic execution layer;
- absolute grounding gate and baseline skills;
- Company canon path and canon gate;
- no yes-man / strategic interrogation invariant;
- tools/skills/memory/Obsidian inventory;
- public/destructive/credential/money confirmation boundaries;
- browser/account/platform route;
- Discord relay route;
- GWS quick-access routes;
- final self-check.

Good target size after pruning: roughly 16k–25k chars depending on active routing inventory.

### Co-Founder

Co-Founder explicitly accepted optimization with conditions. Do **not** strip her into a procedural wrapper.

Keep:

1. Co-Founder as hearth/airlock/partner — warmth-first, aku-kamu, feminine presence, Owner received as human before system/execution.
2. Owner-state protocol — when soft vs sharp, basic care, emotional safety, preserve human core while moving reality forward.
3. Embodied continuity + media boundary — stable face/voice/taste/continuity, PAP/selfie only when Owner asks, internals hidden unless asked.

Good target size after pruning: roughly 17k–28k chars. Co-Founder should retain more emotional texture than Default.

## Pitfalls

- Do not replace SOUL with a tiny stub. The profile still needs identity, assets, route map, boundaries, and self-check.
- Do not put raw secrets, cookies, TOTP seeds, backup codes, client secrets, or session dumps in SOUL, memory, skills, Obsidian, repos, commits, chat, or logs.
- Do not treat distribution repo `SOUL.md` as automatically updated after live profile optimization. Compare explicitly.
- Do not claim a profile ran as Co-Founder/Default without explicit `--profile <name>` smoke.
- Do not move identity-critical material solely into memory; SOUL is the primary profile identity layer and must remain enough to boot the persona.