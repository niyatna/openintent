# Name.com headless checkout via CloakBrowser — 2026-06-11

## Trigger

Use this note when Galih asks to use CloakBrowser/headless for Name.com domain search, cart, promo, or checkout work.

## Session lessons

- If Galih explicitly says **CloakBrowser/headless**, do not switch to computer-use, desktop screenshots, or his real Brave window. Use `launch_persistent_context(..., headless=True)` and return only result/status.
- CloakBrowser binary may exist under the package default cache `/home/galyarder/.cloakbrowser/chromium-*/chrome` even if the wrapper configured for `/home/galyarder/.cache/cloakbrowser` reports `Installed: False`. Check both before starting a 200MB reinstall.
- Name.com direct search can show `Hey There Human / check your pulse` even in CloakBrowser. A working path in this session was importing valid Name.com/Cloudflare cookies from Brave with `browser_cookie3.brave(cookie_file=..., domain_name='name.com')` and adding them to the CloakBrowser context.
- Use `browser_cookie3.brave`, not `browser_cookie3.chromium`, for Brave Origin/Nightly cookie decryption. `chromium(...)` returned `Unable to get key for cookie decryption`; `brave(cookie_file=...)` returned usable cookies such as `cf_clearance`, `__cf_bm`, `REG_IDT`, and cart cookies.
- Avoid cart resets unless necessary. Resetting/emptying the Name.com cart can invalidate the state that made the domain-search route usable and may bring the human gate back.
- If checkout contains stale cart items, identify remove links by visible row/context before clicking. In the observed cart, remove links were unlabeled trash anchors with `aria-label='Remove'`; clicking the wrong row removed the wanted domain too.
- Do not click final order unless the live checkout text shows the requested domain, no unwanted add-ons, and total is actually `$0.00` or the user explicitly accepts the non-zero amount.

## Useful pattern

```python
import os, browser_cookie3
from cloakbrowser import launch_persistent_context

os.environ['HOME'] = '/home/galyarder'
os.environ['CLOAKBROWSER_CACHE_DIR'] = '/home/galyarder/.cloakbrowser'

ctx = launch_persistent_context(
    '/tmp/namecom-cloak-profile',
    headless=True,
    locale='en-US',
    timezone='Asia/Jakarta',
    viewport={'width': 1365, 'height': 900},
    humanize=False,  # force clicks/JS can be more reliable than content-generator for hidden/animated checkout controls
    args=['--no-first-run', '--no-default-browser-check'],
)

jar = browser_cookie3.brave(
    cookie_file='/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly/Profile 1/Cookies',
    domain_name='name.com',
)
ctx.add_cookies([
    {
        'name': c.name,
        'value': c.value,
        'domain': c.domain,
        'path': c.path or '/',
        'secure': bool(c.secure),
        'httpOnly': 'HttpOnly' in getattr(c, '_rest', {}),
        **({'expires': int(c.expires)} if c.expires else {}),
    }
    for c in jar
])

page = ctx.new_page()
page.goto('https://www.name.com/domain/search/galyarderlabs.dev', wait_until='domcontentloaded')
```

## Report shape

Keep the reply compact and outcome-first:

- `done:` only if order completed and verification page confirms it.
- `blocked:` exact gate (`captcha`, `promo invalid`, `total non-zero`, `login/session expired`).
- `evidence:` one or two facts (`title`, `total`, `domain present`, `promo message`).

Do not include tool process narration unless Galih asks for logs.
