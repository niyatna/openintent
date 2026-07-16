# Advanced docs depth and rendered-source verification — 2026-05-23

## Trigger

Use this reference when a public/docs guide has the right IA/slugs but the actual pages feel thin, outline-like, or not genuinely advanced.

Real correction pattern: Owner rejected a docs pass with "isinya pendek pendek banget... apanya yang advanced?". The previous work had the right 23-page Obsidian IA, but several pages were only short outlines. The fix was not another IA change; it was a depth/content-source pass.

## What to do

1. Keep the active IA/slugs unless the user explicitly asks to restructure.
2. Read the source/canon notes again, not just the existing page metadata.
3. Expand the existing markdown files in place into field-manual depth.
4. Use concrete structure per page:
   - context / why it matters;
   - decision rules or matrices;
   - operational checklists/templates;
   - failure modes;
   - maturity path;
   - verification/proof gates.
5. Use subagents for parallel expansion if there are many pages, but verify their writes yourself.
6. Verify source markdown depth with word counts. A useful public field-manual target is roughly 800–1,200+ words per page, unless the page is intentionally narrow.
7. Verify rendered HTML, not only markdown files. The site may have stale data paths, short i18n overrides, generated output, or dynamic-import issues that make the rendered page different from source markdown.
8. Run the docs build/check.
9. Scan for public-safety leaks: private paths, private IDs, secrets, wallet addresses, raw profile instructions, cookies/tokens/TOTP/backup-code/session details, and account recovery details.
10. Scan required source concepts explicitly, not just vibes.

## Astro/static docs pattern

If Astro docs render markdown through a dynamic path like:

```ts
const markdown = await import(`../../content/${doc.slug}.md?raw`);
```

and the page content looks stale/thin, prefer a source manifest:

```ts
const markdownModules = import.meta.glob('../content/*.md', {
  eager: true,
  query: '?raw',
  import: 'default'
}) as Record<string, string>;
```

Then map path -> slug and render from that manifest. This gives the build a static graph of content files.

If locale-specific body overrides exist (for example `contentId`), do not let short localized overrides silently mask the expanded page. Either update them to parity, remove the override, or explicitly report that the locale is still short. Verification must check both source and rendered output for the active locale behavior.

## Verification snippet

A compact verifier for static docs:

```bash
python - <<'PY'
from pathlib import Path
import re
root = Path('src/content')
files = sorted(root.glob('*.md'))
print('slug_count', len(files))
low = []
for p in files:
    wc = len(p.read_text().split())
    if wc < 800:
        low.append((p.name, wc))
    print(f'{p.name:42} {wc:5}')
print('low_under_800', low)
text = '\n'.join(p.read_text() for p in files)
for name, pat in {
    'absolute_private_path': r'/home/|/tmp/|\.hermes|Documents/Obsidian',
    'discord_private_id_like': r'\b\d{17,20}\b',
    'wallet_hex_address_like': r'0x[a-fA-F0-9]{40}',
}.items():
    print(name, [p.name for p in files if re.search(pat, p.read_text(), re.I)])
PY
pnpm build
```

For required concept playwright-pro, search for exact phrases from the source/canon (for example: `AgentKit`, `x402`, `Base`, `Solana`, `cryptographic anchoring`, `Paperclip`, `Hermes Agent`, `MCP`, `Doer`, `Checker`, `Coordinator`, `kill switch`, `ledger event`, `approval`, `budget`, `human review`).

## Reporting style

When the user is angry about quality, do not over-explain the process. Report:

- what was thin/wrong;
- what was expanded;
- exact verification evidence;
- remaining gap if any, especially locale parity.
