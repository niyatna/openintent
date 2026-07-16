#!/usr/bin/env python3
# =============================================================================
# OpenIntent Kit - Discord Niyatna OS Provisioner
# =============================================================================
# Zero-dependency Python script to auto-provision categories and channels 
# for a professional Agentic Company workspace using direct Discord 
# HTTP REST API calls.
# =============================================================================

import os
import sys
import json
import urllib.request
import urllib.error

# Discord Gateway Base API Endpoint
API_BASE = "https://discord.com/api/v10"

def make_request(url, token, method="GET", data=None):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "NiyatnaOS (v1.0.0)"
        },
        method=method
    )
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
        
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err_json = json.loads(body)
            msg = err_json.get("message", body)
        except Exception:
            msg = body
        print(f"HTTP Error {e.code}: {msg}", file=sys.stderr)
        return None, e.code
    except Exception as e:
        print(f"Connection failure: {e}", file=sys.stderr)
        return None, 500

def provision_guild(token, guild_id):
    print(f"\nEvaluating target Guild/Server ID: {guild_id}...")
    
    # Professional Company Rooms channels layout (Clean & Un-alay)
    categories = {
        "GENERAL": {
            "channels": [
                {"name": "announcements", "type": 0},
                {"name": "general-discussion", "type": 0}
            ]
        },
        "OPERATIONS": {
            "channels": [
                {"name": "hq-pulse", "type": 0},
                {"name": "active-tasks", "type": 0},
                {"name": "approval-gates", "type": 0},
                {"name": "proof-of-intent", "type": 0}
            ]
        },
        "DEPARTMENTS": {
            "channels": [
                {"name": "operations-room", "type": 0},
                {"name": "corporate-room", "type": 0},
                {"name": "public-room", "type": 0}
            ]
        },
        "SYSTEM MONITORING": {
            "channels": [
                {"name": "agent-status", "type": 0},
                {"name": "system-logs", "type": 0},
                {"name": "integration-feeds", "type": 0}
            ]
        }
    }

    url_channels = f"{API_BASE}/guilds/{guild_id}/channels"
    
    # Get existing channels to avoid duplicates
    existing, code = make_request(url_channels, token)
    if not existing:
        print("❌ Could not retrieve existing guild channel structures. Aborting.")
        return
        
    existing_names = {c["name"].lower(): c["id"] for c in existing}
    
    for cat_name, cat_data in categories.items():
        cat_id = existing_names.get(cat_name.lower())
        
        if not cat_id:
            print(f"Creating Category: {cat_name}...")
            payload = {"name": cat_name, "type": 4}
            resp, status = make_request(url_channels, token, "POST", payload)
            if resp and "id" in resp:
                cat_id = resp["id"]
                print(f"✅ Created Category '{cat_name}' (ID: {cat_id})")
            else:
                print(f"❌ Failed to create category {cat_name}")
                continue
        else:
            print(f"-> Category '{cat_name}' already exists (ID: {cat_id})")

        # Provision child channels
        for chan in cat_data["channels"]:
            c_name = chan["name"]
            c_type = chan["type"]
            
            c_id = existing_names.get(c_name.lower())
            if not c_id:
                print(f"  Creating Channel: {c_name} (type: {c_type})...")
                payload = {
                    "name": c_name,
                    "type": c_type,
                    "parent_id": cat_id
                }
                
                resp, status = make_request(url_channels, token, "POST", payload)
                if resp and "id" in resp:
                    print(f"  ✅ Created Channel '{c_name}' (ID: {resp['id']})")
                else:
                    print(f"  ❌ Failed to create channel: {c_name}")
            else:
                print(f"  -> Channel '{c_name}' already exists (ID: {c_id})")

    print("\n🎉 Discord workplace setup complete!")

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        # Try reading from root environment variables file relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.abspath(os.path.join(script_dir, "..", ".env"))
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("DISCORD_BOT_TOKEN="):
                        token = line.split("=", 1)[1].strip()
                        break
                        
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable not set.")
        print("Please declare it or run setup.sh first.")
        sys.exit(1)

    # Resolve target guilds the bot is linked to
    guilds, code = make_request(f"{API_BASE}/users/@me/guilds", token)
    
    if not guilds:
        print("❌ Error: Unauthorized. Please verify your DISCORD_BOT_TOKEN is correct.")
        sys.exit(1)

    print("Available Guilds:")
    for idx, g in enumerate(guilds):
        print(f" [{idx}] {g['name']} (ID: {g['id']})")

    if not guilds:
        print("❌ The bot is not joined in any guilds. Inviting link needs usage.")
        sys.exit(1)

    # Prompt for guild unless pre-selected via command line args
    if len(sys.argv) > 1:
        target_id = sys.argv[1]
    else:
        try:
            choice = input(f"\nSelect guild index [0-{len(guilds)-1}] or enter Guild ID: ").strip()
            if choice.isdigit() and int(choice) < len(guilds):
                target_id = guilds[int(choice)]["id"]
            else:
                target_id = choice
        except (KeyboardInterrupt, SystemExit):
            print("\nAborted.")
            sys.exit(0)

    provision_guild(token, target_id)

if __name__ == "__main__":
    main()