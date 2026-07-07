#!/usr/bin/env python3
"""
init_9router_db.py — OpenIntent 9router bootstrap

Creates the initial API key for Niyatna agents by calling 9router's
own POST /api/keys endpoint. This is the correct way — the server
generates the key using its own machineId + HMAC algorithm.

The key is written to /data/.niyatna-9router-key and a .env file
is generated for agent containers to consume via env_file.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = os.environ.get("9ROUTER_API_BASE", "http://localhost:20128")
KEY_NAME = os.environ.get("9ROUTER_KEY_NAME", "niyatna-agent")
KEY_FILE = os.environ.get("9ROUTER_KEY_FILE", "/data/.niyatna-9router-key")
ENV_FILE = os.environ.get("AGENT_ENV_FILE", "/data/.agent.env")
MAX_RETRIES = 30
RETRY_DELAY = 2


def wait_for_9router():
    """Poll 9router until it's ready."""
    url = f"{API_BASE}/api/keys"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print(f"[init] 9router ready (attempt {attempt})")
                    return True
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"[init] waiting for 9router... ({attempt}/{MAX_RETRIES}) {type(e).__name__}")
        time.sleep(RETRY_DELAY)
    print("[init] ERROR: 9router not ready after 60s", flush=True)
    return False


def create_api_key():
    """Create a new API key via POST /api/keys."""
    url = f"{API_BASE}/api/keys"
    body = json.dumps({"name": KEY_NAME}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"[init] key created: id={data.get('id')}, name={data.get('name')}")
            return data.get("key")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[init] ERROR creating key: HTTP {e.code} — {body}", flush=True)
        return None


def save_key(key):
    """Persist the key and generate agent .env file."""
    if not key:
        return False

    # Write the key file
    os.makedirs(os.path.dirname(KEY_FILE) or ".", exist_ok=True)
    with open(KEY_FILE, "w") as f:
        f.write(key.strip() + "\n")
    os.chmod(KEY_FILE, 0o600)
    print(f"[init] key saved to {KEY_FILE}")

    # Write agent .env file for env_file in docker-compose
    with open(ENV_FILE, "w") as f:
        f.write(f"9ROUTER_API_KEY={key.strip()}\n")
    os.chmod(ENV_FILE, 0o600)
    print(f"[init] agent env file written to {ENV_FILE}")

    return True


def main():
    # Check if key already exists (idempotent)
    if os.path.isfile(KEY_FILE):
        existing = open(KEY_FILE).read().strip()
        if existing and existing.startswith("sk-"):
            print(f"[init] key already exists at {KEY_FILE}, skipping")
            return 0

    if not wait_for_9router():
        return 1

    key = create_api_key()
    if not key:
        return 1

    if not save_key(key):
        return 1

    print(f"[init] 9ROUTER_API_KEY={key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())