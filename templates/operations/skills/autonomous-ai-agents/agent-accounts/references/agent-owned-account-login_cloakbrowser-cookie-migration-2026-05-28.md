# CloakBrowser Cookie Migration Pattern

When migrating from legacy Camofox sessions or reviving a stale session where `cookies.json` exists but the CloakBrowser persistent profile is empty/new, use this programmatic pattern to bypass manual login friction.

Instead of automating the full username -> password -> TOTP flow blindly, inject the existing cookies into the new persistent context first. If the session is still valid, the platform will accept it and you just save the updated storage state.

```python
import json, os
from pathlib import Path
from cloakbrowser import launch_persistent_context

def sync_cookies_to_context(ctx, cookie_path):
    if cookie_path.exists() and cookie_path.stat().st_size > 0:
        try:
            cookies = json.loads(cookie_path.read_text())
            if isinstance(cookies, dict) and 'cookies' in cookies:
                cookies = cookies['cookies']
            ctx.add_cookies(cookies)
        except Exception: pass

def sync_context_to_cookies(ctx, cookie_path, storage_path):
    cookies = ctx.cookies()
    cookie_path.parent.mkdir(parents=True, exist_ok=True)
    cookie_path.write_text(json.dumps(cookies, ensure_ascii=False, indent=2))
    os.chmod(cookie_path, 0o600)
    ctx.storage_state(path=str(storage_path))
    os.chmod(storage_path, 0o600)
    return len(cookies)

# Usage inside your run loop:
ctx = launch_persistent_context(str(prof_dir), headless=True, locale="id-ID", timezone="Asia/Jakarta")
try:
    sync_cookies_to_context(ctx, ck_path)
    page = ctx.new_page()
    page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)
    
    # If successfully logged in, immediately sync back to lock in the persistent storage
    sync_context_to_cookies(ctx, ck_path, st_path)
finally:
    ctx.close()
```