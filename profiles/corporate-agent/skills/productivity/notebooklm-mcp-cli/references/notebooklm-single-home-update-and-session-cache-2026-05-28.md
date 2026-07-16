# NotebookLM single-home update + stale MCP session cache (2026-05-28)

Use this reference after updating `notebooklm-mcp-cli` or when Owner asks whether the CLI, MCP integration, and skill docs are correct.

## Canonical single-home state

Do not recreate the deleted profile-home directory.
Do not recreate the old `nlm-default` wrapper.

Current paths:

```text
nlm              OS-home `.local/bin/nlm`
notebooklm-mcp   OS-home `.local/bin/notebooklm-mcp`
credentials      OS-home `.notebooklm-mcp-cli/profiles/default`
```

The active Hermes runtime config, the Default profile config, and the profile MCP mirror should all point NotebookLM MCP to the OS-home `notebooklm-mcp` binary.

## Fast verification ladder

Use this before claiming NotebookLM update/config work is complete:

```bash
set -euo pipefail
export HOME=~/.hermes
export PATH=~/.hermes/.local/bin:$PATH

~/.hermes/.local/bin/nlm --version
~/.hermes/.local/share/uv/tools/notebooklm-mcp-cli/bin/python - <<'PY'
import importlib.metadata as md
print(md.version('notebooklm-mcp-cli'))
PY
~/.hermes/.local/bin/nlm login --check

TMP=$(mktemp)
~/.hermes/.local/bin/nlm notebook list --json > "$TMP"
~/.hermes/.local/share/uv/tools/notebooklm-mcp-cli/bin/python - "$TMP" <<'PY'
import json, sys
items=json.load(open(sys.argv[1]))
print('notebook_count', len(items))
for item in items:
    print(item.get('id'), '|', repr(item.get('title')), '| sources', item.get('source_count'))
PY
rm -f "$TMP"

hermes mcp test notebooklm
```

Important parsing pitfall: when using a Python here-doc, do not pipe `nlm notebook list --json` into the same Python process; the here-doc already consumes stdin for the script body. Write JSON to a temp file, then parse that file.

## Stale current-session MCP server_info

After upgrading the OS-home CLI/MCP binary, current-chat native tools like `mcp_notebooklm_server_info` may still report the old loaded server version. Treat that as current-session MCP cache, not proof the install failed.

Resolution order:

1. Verify the OS-home `nlm --version` and Python package metadata.
2. Verify configured NotebookLM MCP command paths point to the OS-home binary.
3. Run `HOME=~/.hermes hermes mcp test notebooklm` and require connection plus tool discovery.
4. If native tools still show the old version, restart Hermes/gateway or start a fresh session before judging the loaded MCP server.

Do not reinstall, roll back, or recreate profile-home only because `server_info` in the current chat says an old version.

## Reply shape for Owner

For “udah bener belum?” style checks, answer state first:

```text
selesai / partial / belum selesai
- version: ...
- auth: ...
- config path: ...
- MCP tools: ...
- caveat: current-session native MCP may be stale until reload
```

No long process log unless he asks.
