---
author: Galyarder Labs
description: Use when operating the Google NotebookLM workspace programmatic files.
license: MIT
metadata:
  hermes:
    category: productivity
    homepage: https://github.com/jacob-bd/notebooklm-mcp-cli
    related_skills:
    - native-mcp
    - google-workspace
    - youtube-content
    tags:
    - notebooklm
    - mcp
    - cli
    - google
    - research
    - productivity
    - studio
name: notebooklm-mcp-cli
version: 1.0.0
---


# NotebookLM MCP CLI

## Overview

`notebooklm-mcp-cli` provides two interfaces to Google NotebookLM:

- `nlm`: terminal CLI for scripting and one-shot operations.
- `notebooklm-mcp`: MCP server exposing NotebookLM tools to Hermes and other agents.

This Galyarder profile has the package installed and the MCP server configured.

## Local Workspace State

Current single-home install for this machine:

```bash
repo=/home/galyarder/notebooklm-mcp-cli
nlm=/home/galyarder/.local/bin/nlm
notebooklm_mcp=/home/galyarder/.local/bin/notebooklm-mcp
package=notebooklm-mcp-cli==0.6.13
credentials=/home/galyarder/.notebooklm-mcp-cli/profiles/default
hermes_mcp_server=notebooklm
```

Hermes runtime config contains:

```yaml
mcp_servers:
  notebooklm:
    command: /home/galyarder/.local/bin/notebooklm-mcp
    enabled: true
```

Important: this workstation uses the single-home rule. Do **not** recreate `/home/galyarder/.hermes/profiles/galyarder/home`. Prefer OS-home absolute paths and set `HOME=/home/galyarder` in shell checks:

```bash
export HOME=/home/galyarder
export PATH="/home/galyarder/.local/bin:$PATH"
```

For this Galyarder profile, use raw OS-home `nlm` for auth and troubleshooting:

```bash
/home/galyarder/.local/bin/nlm <command>
```

Older references to profile-local `nlm-galyarder` or `/home/galyarder/.hermes/profiles/galyarder/home/...` are historical only. Under the current single-home setup, account-sensitive checks should use:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/nlm login --check
HOME=/home/galyarder /home/galyarder/.local/bin/nlm notebook list --json
```

Observed pitfall: native MCP tools can reflect the server loaded at session start. After updating the CLI/MCP binary, `hermes mcp test notebooklm` or a fresh Hermes session is the proof for the configured runtime path; current-chat native `mcp_notebooklm_*` output may stay stale until the MCP server/session is reloaded.

Current canonical NotebookLM state should be treated as live-verification-dependent, not memory-only. A concise source map, when maintained, lives in Obsidian at `/home/galyarder/Documents/Obsidian Vault/galyarder/galyarder-labs/notebooklm-source-map.md`.

After MCP config changes, restart Hermes/gateway or start a fresh session before expecting native tools like `mcp_notebooklm_*` to reflect the new binary.

Validated smoke-test and use-case recipes live in `references/galyarder-smoke-tests-and-use-cases.md`.

For the 2026-05-28 single-home update, stale current-session MCP `server_info` caveat, and safe verification ladder, see `references/notebooklm-single-home-update-and-session-cache-2026-05-28.md`.

## When to Use

Use this skill for:

- Listing, creating, renaming, deleting, or sharing NotebookLM notebooks.
- Adding sources from URLs, YouTube, text, local files, or Google Drive.
- Querying notebooks and cross-notebook analysis.
- Starting web/Drive research and importing discovered sources.
- Creating studio artifacts: audio overview/podcast, video, report, quiz, flashcards, mind map, slide deck, infographic, data table.
- Downloading or exporting NotebookLM artifacts.
- Troubleshooting auth, stale cookies, MCP connection, or CLI setup.

Do not use for generic Google Drive/Gmail/Docs tasks unless the task specifically involves NotebookLM.

## First Checks

Before performing real NotebookLM operations:

```bash
NLM="$HOME/.local/bin/nlm"
MCP="$HOME/.local/bin/notebooklm-mcp"
"$NLM" --version
"$NLM" doctor --verbose
"$NLM" login --check
hermes mcp test notebooklm
```

If `$HOME/.local/bin/nlm` is missing:

```bash
uv tool install --force notebooklm-mcp-cli
```

To update later:

```bash
uv tool upgrade notebooklm-mcp-cli || uv tool install --force notebooklm-mcp-cli
```

## Auth Protocol

NotebookLM has no official public API. This tool uses NotebookLM internal APIs and browser cookies.

Primary auth:

```bash
"$HOME/.local/bin/nlm" login
"$HOME/.local/bin/nlm" login --check
```

Galyarder profile auth from arbitrary shells:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/nlm login --check
# If credentials are stale, run interactively:
HOME=/home/galyarder /home/galyarder/.local/bin/nlm login
```

Use OS-home `HOME=/home/galyarder` explicitly. The old profile-local `nlm-galyarder` wrapper belonged to the deleted profile-home setup and must not be recreated.

Multi-account profiles:

```bash
nlm login --profile work
nlm login --profile personal
nlm login profile list
nlm login switch work
nlm notebook list --profile work
```

Manual cookie fallback:

```bash
nlm login --manual --file /path/to/cookies.txt
```

MCP fallback after cookies are obtained:

```python
save_auth_tokens(cookies="<cookie_header>")
refresh_auth()
```

Security rules:

- Treat cookies as secrets. Do not print them, summarize them, or store them in notes/memory.
- Do not ask for Google cookies in a public/group chat unless the user explicitly understands the risk; prefer a private channel or local login.
- If auth fails with “Profile not found” or expired cookies, run `nlm login` again.

## Interface Choice

Prefer native MCP tools when they are loaded in the current session because they provide structured parameters and results. In Hermes, discovered tool names use the configured server prefix, typically:

```text
mcp_notebooklm_notebook_list
mcp_notebooklm_source_add
mcp_notebooklm_studio_create
mcp_notebooklm_download_artifact
```

Use CLI via terminal when:

- MCP tools are not loaded yet in the current session.
- You need diagnostics/setup commands (`nlm doctor`, `nlm setup`, `nlm skill`).
- You want shell scripting, piping, or file export.
- Account identity matters and MCP results conflict with what Galih expects.

Galyarder profile correction: if MCP NotebookLM tools show a stale/different notebook list, verify with the OS-home CLI before answering:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/nlm login --check
HOME=/home/galyarder /home/galyarder/.local/bin/nlm notebook list --json
```

Do not say a notebook is missing based only on current-chat MCP output after a CLI/MCP update. If MCP and OS-home CLI disagree, trust the fresh CLI/runtime `hermes mcp test notebooklm` first and investigate MCP session reload/profile drift.

Never use `nlm chat start` in agent contexts. It opens an interactive REPL. Use one-shot query instead:

```bash
nlm notebook query <notebook-id> "question"
```

## Safety Rules

Destructive operations require explicit user confirmation after showing the exact target:

- `notebook_delete` / `nlm notebook delete <id> --confirm`
- `source_delete` / `nlm source delete <id> --confirm`
- `studio_delete` / `nlm studio delete <notebook-id> <artifact-id> --confirm`
- `note(... action="delete")`

Generation operations can consume quota/time and require `confirm=True` or `--confirm`. Before generating large artifacts, summarize settings and get user approval when cost/time matters.

Rate-limit posture:

- Free tier is limited; avoid unnecessary repeated queries.
- Add a small delay between source additions in scripts.
- Prefer batch operations where possible.

## Common CLI Commands

Use absolute binary if needed:

```bash
NLM="$HOME/.local/bin/nlm"
```

Notebooks:

```bash
$NLM notebook list
$NLM notebook list --json
$NLM notebook create "Research Project"
$NLM notebook get <notebook-id>
$NLM notebook rename <notebook-id> "New Title"
$NLM notebook query <notebook-id> "What are the main takeaways?"
$NLM notebook delete <notebook-id> --confirm
```

Sources:

```bash
$NLM source list <notebook-id>
$NLM source add <notebook-id> --url "https://example.com/article" --wait
$NLM source add <notebook-id> --url "https://youtube.com/watch?v=..." --wait
$NLM source add <notebook-id> --text "content" --title "Notes"
$NLM source add <notebook-id> --file ./document.pdf --wait
$NLM source add <notebook-id> --drive <doc-id> --type doc
$NLM source content <source-id> --output ./source.txt
$NLM source stale <notebook-id>
$NLM source sync <notebook-id> --confirm
```

Research:

```bash
$NLM research start "query" --notebook-id <notebook-id> --mode fast
$NLM research start "query" --notebook-id <notebook-id> --mode deep
$NLM research status <notebook-id> --max-wait 300
$NLM research import <notebook-id> <task-id>
```

Studio artifacts:

```bash
$NLM audio create <notebook-id> --format deep_dive --length default --confirm
$NLM video create <notebook-id> --format brief --style whiteboard --confirm
$NLM report create <notebook-id> --format "Briefing Doc" --confirm
$NLM quiz create <notebook-id> --count 10 --difficulty medium --confirm
$NLM flashcards create <notebook-id> --difficulty hard --confirm
$NLM mindmap create <notebook-id> --confirm
$NLM slides create <notebook-id> --confirm
$NLM infographic create <notebook-id> --orientation landscape --style professional --confirm
$NLM data-table create <notebook-id> --description "Extract key dates and events" --confirm
$NLM studio status <notebook-id>
```

Downloads/exports:

```bash
$NLM download audio <notebook-id> <artifact-id> --output podcast.mp3
$NLM download video <notebook-id> <artifact-id> --output video.mp4
$NLM download report <notebook-id> <artifact-id> --output report.md
$NLM download slide-deck <notebook-id> <artifact-id> --format pptx --output slides.pptx
$NLM export docs <notebook-id> <artifact-id> --title "Report"
$NLM export sheets <notebook-id> <artifact-id> --title "Data Table"
```

Aliases and tags:

```bash
$NLM alias set myproject <notebook-id>
$NLM alias list
$NLM tag add <notebook-id> --tags "ai,research"
$NLM tag select "ai research"
```

## MCP Tool Map

Core tools exposed by the `notebooklm` MCP server:

- Auth: `refresh_auth`, `save_auth_tokens`, `server_info`
- Notebooks: `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`, `notebook_query`, `notebook_query_start`, `notebook_query_status`, `notebook_rename`, `notebook_delete`
- Sources: `source_add`, `source_list_drive`, `source_sync_drive`, `source_rename`, `source_delete`, `source_describe`, `source_get_content`
- Studio: `studio_create`, `studio_status`, `studio_delete`, `studio_revise`, `download_artifact`, `export_artifact`
- Research: `research_start`, `research_status`, `research_import`
- Notes/sharing: `note`, `notebook_share_status`, `notebook_share_public`, `notebook_share_invite`, `notebook_share_batch`
- Advanced: `batch`, `cross_notebook_query`, `pipeline`, `tag`, `label`, `chat_configure`

Typical MCP source add:

```python
source_add(
  notebook_id="...",
  source_type="url",
  url="https://...",
  wait=True,
  wait_timeout=120.0,
)
```

Typical MCP artifact creation:

```python
studio_create(
  notebook_id="...",
  artifact_type="audio",
  audio_format="deep_dive",
  audio_length="default",
  confirm=True,
)
studio_status(notebook_id="...")
download_artifact(notebook_id="...", artifact_type="audio", output_path="podcast.mp3")
```

## Troubleshooting

If the user pasted Google cookies into chat, treat them as compromised session secrets. Do not repeat, quote, summarize, save, or add them to memory. Recommend revoking/logging out that Google session if the account matters. Prefer browser/CDP login or a local private cookie file. For historical Brave Origin Nightly/profile-home debugging context, see `references/brave-origin-nightly-profile-home.md`, but do not recreate profile home under the current single-home setup.

If CLI works but MCP tools do not appear:

```bash
hermes mcp list
hermes mcp test notebooklm
```

Then restart Hermes/gateway or start a fresh session.

If MCP is missing from config:

```bash
hermes mcp add notebooklm --command "$HOME/.local/bin/notebooklm-mcp"
hermes mcp test notebooklm
```

If authentication fails:

```bash
nlm login --check || nlm login
nlm login profile list
nlm doctor --verbose
```

If `nlm login` cannot find a browser but Brave/CloakBrowser exists, keep `HOME=/home/galyarder`, inspect browser availability, and use manual cookie/browser fallback without creating `/home/galyarder/.hermes/profiles/galyarder/home`. The old `nlm-galyarder` wrapper path is historical only.

If source/notebook ID fails:

```bash
nlm notebook list --title
nlm source list <notebook-id> --title
nlm alias list
```

If research is already running:

```bash
nlm research status <notebook-id> --full
nlm research import <notebook-id> <task-id>
# or start a new one only if intended:
nlm research start "query" --notebook-id <notebook-id> --force
```

## Verification Checklist

Before claiming a NotebookLM task is complete:

- [ ] Installation verified with `nlm --version` or `hermes mcp test notebooklm`.
- [ ] Auth verified with `nlm login --check` or a successful MCP auth-dependent call.
- [ ] Notebook/source/artifact IDs captured and reused correctly.
- [ ] Destructive actions had explicit user confirmation.
- [ ] Generated/downloaded files exist at the reported path when applicable.
- [ ] Final response includes exact notebook/source/artifact IDs or file paths needed for follow-up.
