# Historical profile-home NotebookLM auth quirk

This reference is preserved only as historical debugging context from the old profile-home setup.

## Current state

Default now follows the single-home rule:

```bash
export HOME=~/.hermes
NLM=~/.hermes/.local/bin/nlm
MCP=~/.hermes/.local/bin/notebooklm-mcp
```

Do **not** recreate `~/.hermes/profiles/default/home`.
Do **not** recreate the old profile-local `nlm-default` wrapper.
Credentials intentionally live under:

```text
~/.hermes/.notebooklm-mcp-cli/profiles/default
```

## Historical symptoms

Older `notebooklm-mcp-cli==0.6.3` plus profile-home isolation had these issues:

- `nlm login` could fail to detect Brave Origin Nightly.
- Auth could land in the wrong `Path.home()` directory.
- The helper wrapper `nlm-default` forced a profile-local `HOME`.

Those fixes are obsolete for this workstation after the single-home migration.

## Current troubleshooting posture

If auth fails now:

```bash
HOME=~/.hermes ~/.hermes/.local/bin/nlm login --check
HOME=~/.hermes ~/.hermes/.local/bin/nlm login
HOME=~/.hermes ~/.hermes/.local/bin/nlm doctor --verbose
```

If MCP seems stale after an update:

```bash
HOME=~/.hermes hermes mcp list
HOME=~/.hermes hermes mcp test notebooklm
```

Then restart Hermes/gateway or start a fresh session if native `mcp_notebooklm_*` tools are still serving an old loaded server.

## Security note

If the user pasted Google cookies into chat, treat them as compromised session secrets. Do not repeat, summarize, store, or add them to memory. Prefer local browser login or a private local cookie file.
