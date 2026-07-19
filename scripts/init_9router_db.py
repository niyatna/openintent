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
    """Poll 9router endpoint until the server is running and the database is initialized."""
    # First, make a public health check request to `/api/health` to wait for HTTP server readiness
    health_url = f"{API_BASE}/api/health"
    print(f"[init] waiting for 9router HTTP server at {health_url}...", flush=True)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(health_url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print(f"[init] 9router HTTP server is up (attempt {attempt})", flush=True)
                    break
        except Exception as e:
            pass
        time.sleep(RETRY_DELAY)
    else:
        print("[init] ERROR: 9router HTTP server not ready after 60s", flush=True)
        return False

    # Second, trigger lazy database initialization by calling /api/keys (which runs DB migrations)
    trigger_url = f"{API_BASE}/api/keys"
    print(f"[init] triggering 9router database initialization at {trigger_url}...", flush=True)
    try:
        req = urllib.request.Request(trigger_url, method="GET")
        # This will return 401 Unauthorized, but will trigger database migrations to run
        with urllib.request.urlopen(req, timeout=5) as resp:
            pass
    except Exception as e:
        # Expected to fail with 401, which is fine
        pass

    # Third, wait for the database file to be written to disk
    db_path = "/data/db/data.sqlite"
    for attempt in range(1, MAX_RETRIES + 1):
        if os.path.exists(db_path):
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0].lower() for row in cursor.fetchall()]
                conn.close()
                if "apikeys" in tables:
                    print(f"[init] 9router SQLite database initialized (attempt {attempt})", flush=True)
                    return True
            except Exception as e:
                print(f"[init] db file exists but not fully migrated: {e} ({attempt}/{MAX_RETRIES})", flush=True)
        else:
            print(f"[init] waiting for SQLite database file at {db_path}... ({attempt}/{MAX_RETRIES})", flush=True)
        time.sleep(RETRY_DELAY)
        
    print("[init] ERROR: 9router database file not found after 60s", flush=True)
    return False


def create_api_key():
    """Create a new API key directly in the SQLite database."""
    import sqlite3
    import uuid
    import datetime
    
    db_path = "/data/db/data.sqlite"
    key = "sk-niyatna-agent-" + uuid.uuid4().hex[:12]
    key_id = str(uuid.uuid4())
    created_at = datetime.datetime.utcnow().isoformat() + "Z"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO apiKeys (id, key, name, machineId, isActive, createdAt) VALUES (?, ?, ?, ?, ?, ?)",
            (key_id, key, KEY_NAME, "niyatna-bootstrap", 1, created_at)
        )
        conn.commit()
        conn.close()
        print(f"[init] direct DB: key created: id={key_id}, name={KEY_NAME}")
        return key
    except Exception as e:
        print(f"[init] ERROR inserting key directly into database: {e}", flush=True)
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
        key_val = key.strip()
        f.write(f"9ROUTER_API_KEY={key_val}\n")
        f.write(f"HINDSIGHT_API_KEY={key_val}\n")
        f.write(f"HINDSIGHT_API_LLM_API_KEY={key_val}\n")
        f.write(f"HINDSIGHT_LLM_API_KEY={key_val}\n")
    os.chmod(ENV_FILE, 0o600)
    print(f"[init] agent env file written to {ENV_FILE}")
    return True


def seed_9router_db():
    """Dynamically seed 9router's SQLite database with OpenRouter key if present."""
    db_path = "/data/db/data.sqlite"
    or_key = os.environ.get("OPENROUTER_API_KEY")
    if not or_key or not os.path.exists(db_path):
        print(f"[init] openrouter key missing or database not found at {db_path}, skipping seed")
        return

    import sqlite3
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Scan tables list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0].lower() for row in cursor.fetchall()]
        print(f"[init] detected 9router tables: {tables}")
        
        # 9router standard structures for keys/providers
        if "keys" in tables:
            # check if openrouter key needs update/insert
            cursor.execute("SELECT id FROM keys WHERE provider='openrouter'")
            res = cursor.fetchone()
            if res:
                cursor.execute("UPDATE keys SET credential=? WHERE provider='openrouter'", (or_key,))
                print("[init] updated openrouter credential in 'keys' table")
            else:
                cursor.execute("INSERT OR REPLACE INTO keys (provider, credential) VALUES ('openrouter', ?)", (or_key,))
                print("[init] inserted openrouter credential in 'keys' table")
        elif "providers" in tables:
            # check if openrouter key matches providers table structure
            cursor.execute("SELECT id FROM providers WHERE name='openrouter'")
            res = cursor.fetchone()
            if res:
                cursor.execute("UPDATE providers SET key=? WHERE name='openrouter'", (or_key,))
                print("[init] updated openrouter key in 'providers' table")
            else:
                cursor.execute("INSERT OR REPLACE INTO providers (name, key) VALUES ('openrouter', ?)", (or_key,))
                print("[init] inserted openrouter key in 'providers' table")
        else:
            print("[init] no matching providers/keys table found in 9router database schema")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[init] WARNING: could not seed SQLite db: {e}")


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

    # Inject OpenRouter key to sqlite DB
    seed_9router_db()
    print(f"[init] 9ROUTER_API_KEY={key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())