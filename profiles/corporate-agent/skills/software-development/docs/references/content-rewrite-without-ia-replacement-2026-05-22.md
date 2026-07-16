# Content rewrite without IA replacement — 2026-05-22

## Trigger

User asked to rewrite all content and add what was missing so an existing docs site became more complete and advanced according to Obsidian source docs.

The intended meaning was **rewrite/expand the existing docs in place**, not rebuild the information architecture or replace existing pages.

## Failure mode observed

A delegated content agent:

- archived existing active markdown pages to `*.archived`;
- generated many new slugs/pages;
- changed `docs.ts` to point at the new IA;
- reported build success;
- missed that the user wanted existing content rewritten, not a new docs structure.

The build passing did not mean the requested content model was preserved.

## Recovery pattern

1. Inspect active docs and generated replacements.
2. Restore archived originals over the active filenames.
3. Remove generated replacement-only active docs that were not part of the original page model.
4. Rewrite the existing files in place, integrating missing source concepts into current pages.
5. Update metadata, nav/home/footer/i18n to match the refined framing.
6. Build.
7. Scan for:
   - active markdown count and slug set;
   - required source concepts;
   - forbidden or stale public-framing terms.

## Rule for future docs rewrites

When user says `rewrite`, `more complete`, `more advanced`, or `add what is missing`, default to **in-place rewrite and section expansion**.

Only create a new IA or new docs pages if:

- the user explicitly requests new structure/pages; or
- the existing page model cannot hold the required material; and
- you preserve active pages unless the user approves removal/rename.

## Delegation prompt requirements

If using a subagent, include:

```text
Active docs/slugs must be preserved unless explicitly stated otherwise:
<list slugs>

Do not archive, delete, rename, or replace active docs.
Rewrite current docs in place.
Add new sections inside existing docs first.
Add new docs only if absolutely necessary, and report why.
Return before/after active slug list.
```

## Verification commands/patterns

```bash
# active source docs only
python - <<'PY'
from pathlib import Path
p=Path('src/content')
print(sorted(x.name for x in p.glob('*.md') if not x.name.startswith('_')))
PY

# build
pnpm build

# scan required concepts and stale language
python - <<'PY'
from pathlib import Path
import re
root=Path('src')
text='\n'.join(p.read_text(errors='ignore') for p in root.rglob('*') if p.suffix in {'.md','.ts','.astro'})
for term in ['Agentic SaaS','persistent identity','controlled money','verifiable records','human-governed','AgentKit','x402','Base','Solana','spending limit','ledger event','cryptographic anchoring','balance sheet','cashflow','legal','compliance']:
    print(term, len(re.findall(re.escape(term), text, re.I)))
for term in ['Agent OS','Agentic Company Stack','control plane','operator layer','operating layer']:
    print('stale', term, len(re.findall(re.escape(term), text, re.I)))
PY
```
