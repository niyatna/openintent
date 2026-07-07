---
name: obsidian
description: Use when reading, writing, searching, or syncing Obsidian vault notes, configuring .canvas/json layouts, managing database bases files, or running CLI plugin operations.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [note-taking, obsidian, markdown, vault-architect, obsidian, obsidian]
    category: note-taking
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

For mobile sync / same-WiFi phone access to Obsidian, use the Syncthing workflow in `references/syncthing-mobile-sync.md`. Do not stop after device pairing; verify folder IDs match across devices and that Obsidian opens the same synced path.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

Galyarder profile convention:

- Galyarder personal/strategic notes that Galih may need to read later go under `/home/galyarder/Documents/Obsidian Vault/galyarder/`.
- Notes specifically about Galyarder Labs go under `/home/galyarder/Documents/Obsidian Vault/galyarder/galyarder-labs/`.
- Keiya-specific emotional/relational notes use the Keiya vault path, not the Galyarder path.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

For Galyarder system continuity, create notes when a correction, runbook, decision, source map, or multi-session protocol needs to be human-readable later. Do not answer "that belongs in memory" as a reason to skip Obsidian; memory/Hindsight and Obsidian serve different layers. Use concise Obsidian notes for readable audit/continuity, and still use Hindsight/hot memory for recall/runtime behavior as appropriate.

Useful Galyarder folder conventions:

```text
galyarder/operating-protocols/
galyarder/system-notes/
galyarder/galyarder-labs/
```

Examples created from a system-continuity session:

- `operating-protocols/galyarder-memory-and-obsidian-protocol.md`
- `system-notes/hermes-hindsight-operational-state.md`
- `system-notes/system-corrections-rtk-notebooklm-proof-paths.md`
- `galyarder-labs/notebooklm-source-map.md`

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## References & Sub-playbooks
- `references/obsidian.md` — Garden mapping paradigms and visual workflows
- `references/obsidian.md` — Callouts formatting, embeds, and wikilinks parsing
- `references/obsidian.md` — Database table / card view configurations
- `references/obsidian.md` — Creating raw visual canvases and structural flowcharts
- `references/obsidian.md` — CLI searching, plugin developments, and theme setups
