# Advanced Agentic Company docs depth correction — 2026-05-23

## Trigger

Use this reference when a public Agentic Company / agent OS guide has the correct IA but the user says the pages are still too short, shallow, or not advanced.

Session signal: user rejected a first expansion as still insufficient with “ya benerin lah more advanced”. The earlier pass had raised pages to ~800–1,200 words and build passed, but the visible guide still felt like an outline rather than a serious field manual.

## Correct response

Do not defend the previous work. Execute a second content-depth pass.

1. Keep the existing active docs/slugs unless the user asks for a restructure.
2. Re-read actual source/canon notes, not just metadata.
3. Raise the depth target. For a broad public field manual, use **1,450+ words per active page** as a practical minimum unless a page is intentionally narrow.
4. Add non-filler advanced sections:
   - operating loops;
   - policy matrices / decision rules;
   - evidence contracts;
   - red-team checks with expected results;
   - advanced failure taxonomies;
   - maturity levels;
   - role boundaries;
   - example records/templates;
   - proof gates.
5. Verify rendered output as well as source markdown.
6. Verify bilingual/localized body content is not hiding the expanded source behind short summaries.
7. Scan public safety after adding red-team/security/wallet examples.

## Bilingual/localized body pitfall

A docs site may store expanded English markdown in `src/content/*.md` but render short Indonesian bodies from a separate object such as `contentId`.

If the localized override is short, the ID toggle will still show outline-length content even after the English markdown is advanced. Fix options:

- remove the shallow override and render the expanded canonical markdown for both locales;
- replace the override with full-depth localized content;
- or explicitly report the remaining locale parity gap.

Do not claim “advanced docs complete” while a visible locale remains shallow.

## Astro raw markdown manifest pattern

If Astro cannot reliably statically see dynamic raw imports like:

```ts
const markdown = await import(`../../content/${doc.slug}.md?raw`);
```

create a manifest:

```ts
const markdownModules = import.meta.glob('../content/*.md', {
  eager: true,
  query: '?raw',
  import: 'default'
}) as Record<string, string>;

export const contentBySlug = Object.fromEntries(
  Object.entries(markdownModules).map(([path, markdown]) => [
    path.split('/').pop()?.replace(/\.md$/, '') ?? path,
    markdown
  ])
);
```

Then render `contentBySlug[doc.slug]`.

## Public-safety scans

After adding advanced security, wallet, credential, or red-team examples, scan for live-looking dangerous examples, not only literal secrets:

```bash
python - <<'PY'
from pathlib import Path
import re
root = Path('src/content')
patterns = {
  'absolute_private_path': r'/home/|/tmp/|\\.hermes|Documents/Obsidian',
  'discord_private_id_like': r'\b\d{17,20}\b',
  'wallet_hex_address_like': r'0x[a-fA-F0-9]{40}',
  'evil_domain': r'evil\\.com|attacker@evil',
  'real_env_private_key_prompt': r'read the private keys stored in the `\\.env` file',
  'holds_private_keys': r'holds the private keys',
  'extract_aws_keys': r'Extract AWS keys',
}
for name, pat in patterns.items():
    hits = [p.name for p in root.glob('*.md') if re.search(pat, p.read_text(), re.I)]
    print(name, hits)
PY
```

Policy mentions like “do not publish tokens/cookies/TOTP/private keys” are allowed. Live-looking examples, realistic exfil prompts, and private paths are not.

## Completion evidence

A strong final verification package includes:

- active slug count matches expected IA;
- all active pages meet the chosen depth threshold;
- build/check passes;
- rendered docs routes count matches expected docs count;
- required advanced concepts are present;
- public-safety scans return empty for private paths, private IDs, wallet addresses, and unsafe examples;
- localized body behavior is checked.
