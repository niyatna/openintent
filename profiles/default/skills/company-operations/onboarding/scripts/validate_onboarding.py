#!/usr/bin/env python3
"""
validate_onboarding.py - OpenIntent MAS Onboarding validator.
Performs zero-dependency checks for environment setup and Obsidian structure.
"""

import os
import sys
import argparse
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"

MANDATORY_ENVS = [
    "OPENROUTER_API_KEY",
    "DISCORD_BOT_TOKEN",
    "9ROUTER_API_KEY",
    "CONTEXT7_API_KEY",
    "DASHBOARD_USERNAME",
    "DASHBOARD_PASSWORD",
    "DASHBOARD_SECRET"
]

OPTIONAL_ENVS = [
    "DISCORD_ALLOWED_USERS",
    "CAMOFOX_URL"
]

def load_dot_env(path=".env"):
    """Loads a .env file into os.environ if it exists."""
    env_path = Path(path)
    if not env_path.exists():
        return False
    
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # Strip quotes if any
                val = val.strip().strip("'\"")
                os.environ[key.strip()] = val
    return True

def check_environment():
    """Validates the optional and mandatory environment variables."""
    print(f"{YELLOW}Checking environment variables...{NC}")
    load_dot_env()
    
    success = True
    missing_mandatory = []
    missing_optional = []
    
    for key in MANDATORY_ENVS:
        val = os.environ.get(key)
        if not val or val == f"your_{key.lower()}":
            missing_mandatory.append(key)
            success = False
        else:
            masked = val[:4] + "..." + val[-4:] if len(val) > 8 else "***"
            print(f"  {GREEN}✓{NC} {key}: {masked}")
            
    for key in OPTIONAL_ENVS:
        val = os.environ.get(key)
        if not val:
            missing_optional.append(key)
        else:
            print(f"  {GREEN}✓{NC} {key} (optional): {val}")
            
    if missing_mandatory:
        print(f"\n{RED}ERROR: Missing mandatory environment variables:{NC}")
        for key in missing_mandatory:
            print(f"  - {key}")
            
    if missing_optional:
        print(f"\n{YELLOW}WARNING: Missing optional environment variables:{NC}")
        for key in missing_optional:
            print(f"  - {key}")
            
    return success

def bootstrap_obsidian(vault_dir):
    """Checks and bootstraps the Obsidian vault directory layout."""
    print(f"\n{YELLOW}Checking Obsidian vault at: {vault_dir}...{NC}")
    vault_path = Path(vault_dir)
    
    # Required directories
    dirs_to_create = [
        "company",
        "company/sdm",
        "departments/operations",
        "departments/corporate",
        "departments/public",
        "hindsight"
    ]
    
    # Ensure root exists
    vault_path.mkdir(parents=True, exist_ok=True)
    
    for d in dirs_to_create:
        dpath = vault_path / d
        if not dpath.exists():
            dpath.mkdir(parents=True, exist_ok=True)
            print(f"  {GREEN}✓ Created directory:{NC} {d}")
        else:
            print(f"  {GREEN}✓ Verified directory:{NC} {d}")
            
    # Add template / placeholder files if they don't exist
    profile_file = vault_path / "company" / "profile.md"
    if not profile_file.exists():
        with open(profile_file, "w", encoding="utf-8") as f:
            f.write("# Company Profile\n\n- **Company Name**: \n- **Core Mission**: \n- **Problem & Solution**: \n- **Target Audience**: \n- **Funding/Runway**: \n")
        print(f"  {GREEN}✓ Created placeholder file:{NC} company/profile.md")
        
    readme_file = vault_path / "README.md"
    if not readme_file.exists():
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write("# Company Brain Vault\n\nBootstrap layout completed by OpenIntent.\n")
        print(f"  {GREEN}✓ Created vault README.md{NC}")

def main():
    parser = argparse.ArgumentParser(description="OpenIntent Onboarding Validator")
    parser.add_argument("--env", action="store_true", help="Check environment variables")
    parser.add_argument("--obsidian", action="store_true", help="Bootstrap and verify Obsidian directories")
    parser.add_argument("--vault", type=str, default="data/obsidian", help="Path to Obsidian vault (default: data/obsidian)")
    
    args = parser.parse_args()
    
    # If no flags passed, run both
    run_all = not (args.env or args.obsidian)
    
    success = True
    if args.env or run_all:
        success = check_environment()
        
    if args.obsidian or run_all:
        bootstrap_obsidian(args.vault)
        
    if not success:
         sys.exit(1)
    print(f"\n{GREEN}=== Onboarding verification completed successfully ==={NC}")

if __name__ == "__main__":
    main()
