# Static Docs / Public-Safe Site Verification

Use this when finishing a static documentation or public-guide site, especially when the site adapts private operating patterns into publishable material.

## What This Proves

- local preview serves the intended artifact
- internal links/assets resolve
- the published files do not contain obvious live secrets, private paths, raw account state, or internal IDs
- public-safety language is documentation, not a leaked credential
- deployment remains confirmation-gated until the user approves target + exact copy

## Minimum Verification Ladder

1. **Start or confirm local server**
   - Serve from the project root, bound to localhost.
   - If a server is already running, poll/check it rather than starting a duplicate.

2. **Crawl internal site graph**
   - Fetch `/` and every same-origin `href`/`src` found in HTML.
   - Require HTTP `200` for every internal HTML, CSS, JS, markdown/template, and asset link.
   - Report visited URL count and crawl error count.

3. **Scan for actual leakage**
   - Scan project files excluding `.git/`.
   - Use high-signal patterns for live-looking secrets and private artifacts:
     - OpenAI-style `sk-...`
     - GitHub `ghp_`, `github_pat_`, `gho_`, `ghu_`, `ghs_`, `ghr_`
     - Slack `xox...`
     - AWS `AKIA...`
     - Google API `AIza...`
     - private key blocks
     - raw cookie/session field values such as `auth_token=...`, `ct0=...`, `sessionid=...`
     - internal private paths like `/home/galyarder/.hermes/private`, local GWS config dirs, private vault paths
     - long Discord snowflakes / raw account IDs when not meant for public docs
   - Do **not** treat educational words like `token`, `backup code`, `TOTP`, `cookie`, or `secret` as leaks by themselves when they appear in no-publish/security outlines. Count them as policy text unless paired with a live-looking value.

4. **Check repository state without mutating**
   - Run `git status --short --branch`.
   - Count public files excluding `.git/`.
   - Do not commit or deploy unless the user explicitly asked for that side effect.

5. **Final report shape**
   - artifact path
   - preview URL
   - key directories/files
   - local server status
   - crawl result: visited count, failures
   - leakage scan result: files scanned, leak count
   - git state
   - explicit publication gate: not deployed/not public unless approved

## Compact Python Crawl + Scan Pattern

Use a small script from the project root or via `execute_code` when available:

```python
from pathlib import Path
import re, urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

root = Path('/path/to/site')
base = 'http://127.0.0.1:8765/'

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('href', 'src') and v and not v.startswith('#'):
                self.links.append(v)

def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.status, r.read(), r.headers.get('content-type', '')

visited, queue, errors, statuses = set(), [base], [], []
while queue:
    url = queue.pop(0)
    if url in visited: continue
    visited.add(url)
    try:
        status, data, ctype = fetch(url)
        statuses.append((url, status, len(data), ctype))
        if 'text/html' in ctype:
            p = LinkParser(); p.feed(data.decode('utf-8', 'ignore'))
            for link in p.links:
                if link.startswith(('http://', 'https://', 'mailto:')): continue
                next_url = urljoin(url, link)
                if urlparse(next_url).netloc == urlparse(base).netloc and next_url not in visited:
                    queue.append(next_url)
    except Exception as e:
        errors.append((url, repr(e)))

patterns = {
    'openai_sk': r'\bsk-[A-Za-z0-9_-]{20,}\b',
    'github_pat': r'\b(?:ghp|github_pat|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b',
    'slack_token': r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
    'aws_access_key': r'\bAKIA[0-9A-Z]{16}\b',
    'google_api_key': r'\bAIza[0-9A-Za-z_-]{35}\b',
    'private_key_block': r'-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----',
    'raw_session_cookie': r'\b(?:auth_token|ct0|sessionid|csrftoken)\s*[:=]\s*[A-Za-z0-9_%.-]{8,}',
    'private_path': r'/home/galyarder/(?:\.hermes/private|\.config/gws[^\s"\']*|Documents/Obsidian Vault/[^\s"\']*)',
    'raw_snowflake': r'\b\d{17,20}\b',
}
leaks = []
for p in root.rglob('*'):
    if not p.is_file() or '.git/' in str(p): continue
    text = p.read_text('utf-8', errors='ignore')
    for name, pat in patterns.items():
        for m in re.finditer(pat, text, flags=re.I):
            leaks.append((str(p.relative_to(root)), name, m.group(0)[:120]))

print('crawl_visited', len(visited))
print('crawl_errors', len(errors))
print('files_scanned', sum(1 for p in root.rglob('*') if p.is_file()))
print('actual_secret_leaks', len(leaks))
for item in leaks:
    print('LEAK', item)
if errors or leaks:
    raise SystemExit(1)
```

## Common Pitfalls

- Treating words like `backup codes` in a no-publish checklist as an actual secret leak.
- Declaring a site public-safe after checking only `index.html`.
- Committing/deploying because verification passed when the user only asked for a local artifact.
- Reporting `done` without separating **local verification** from **publication approval**.
- Trusting compacted task state without rerunning the crawl/scan fresh before final status.
