#!/usr/bin/env python3
"""Create a private agent-owned account credential skeleton without secrets.

The script writes only placeholders unless explicit non-secret values are passed.
It never asks for or prints passwords, TOTP secrets, backup codes, tokens, cookies,
or wallet secrets.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
from pathlib import Path

DEFAULT_ROOT = Path("/home/galyarder/.hermes/private/credentials/agents")
SERVICES = {"google", "gmail", "github", "x", "twitter", "notion", "linear", "wallet", "discord", "email"}
SECRET_PLACEHOLDERS = {
    "PASSWORD": "",
    "TOTP_SECRET": "",
}


def chmod_private(path: Path, mode: int) -> None:
    path.chmod(mode)


def safe_segment(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    if not cleaned:
        raise ValueError("empty path segment")
    return cleaned


def account_id(owner: str, service: str, label: str | None) -> str:
    parts = [safe_segment(owner), safe_segment(service)]
    if label:
        parts.append(safe_segment(label))
    return "-".join(parts)


def render_account_file(*, owner: str, service: str, account_id_value: str, email: str, username: str, label: str, directory: Path) -> str:
    backup_codes = directory / "backup-codes.txt"
    cookies = directory / "cookies.json"
    lines = [
        "# Agent-owned account credential file.",
        "# chmod 600. Never commit, paste, screenshot, or print secret values.",
        "# Fill secrets locally only after Galih approves the account contract.",
        f"ACCOUNT_ID={account_id_value}",
        f"OWNER={owner}",
        f"SERVICE={service}",
        f"EMAIL={email}",
        f"USERNAME={username}",
        f"LABEL={label}",
        f"PASSWORD={SECRET_PLACEHOLDERS['PASSWORD']}",
        f"TOTP_SECRET={SECRET_PLACEHOLDERS['TOTP_SECRET']}",
        f"BACKUP_CODES_FILE={backup_codes}",
        f"COOKIES_FILE={cookies}",
        "RECOVERY_EMAIL=",
        "PHONE_LAST4=",
        "NOTES=dedicated agent-owned account; secrets are local-only",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create private account.txt skeleton")
    parser.add_argument("--owner", required=True, help="keiya, galyarder, or another dedicated agent owner")
    parser.add_argument("--service", required=True, help="google, github, x, notion, linear, wallet, etc.")
    parser.add_argument("--label", default="", help="optional non-secret label, e.g. labs")
    parser.add_argument("--email", default="", help="optional non-secret email identifier")
    parser.add_argument("--username", default="", help="optional non-secret username identifier")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--force", action="store_true", help="overwrite existing account.txt skeleton")
    args = parser.parse_args()

    owner = safe_segment(args.owner)
    service = safe_segment(args.service)
    if service not in SERVICES:
        # Allow future services but make the operator notice.
        service_warning = f"unrecognized service '{service}', continuing with generic skeleton"
    else:
        service_warning = ""

    root = Path(args.root)
    directory = root / owner / service
    directory.mkdir(parents=True, exist_ok=True)
    chmod_private(root, 0o700)
    # Ensure all path parents under the private root are private when they exist.
    current = root
    for part in directory.relative_to(root).parts:
        current = current / part
        chmod_private(current, 0o700)

    acct_id = account_id(owner, service, args.label or None)
    account_path = directory / "account.txt"
    if account_path.exists() and not args.force:
        result = {"ok": False, "error": "account.txt already exists", "account_file": str(account_path), "hint": "rerun with --force only if you intend to overwrite placeholders"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1

    content = render_account_file(owner=owner, service=service, account_id_value=acct_id, email=args.email, username=args.username, label=args.label, directory=directory)
    account_path.write_text(content, encoding="utf-8")
    chmod_private(account_path, 0o600)

    # Create empty placeholders with private permissions. These files are runtime-only.
    backup_path = directory / "backup-codes.txt"
    if not backup_path.exists():
        backup_path.write_text("# one backup code per line; keep local-only\n", encoding="utf-8")
        chmod_private(backup_path, 0o600)
    cookies_path = directory / "cookies.json"
    if not cookies_path.exists():
        cookies_path.write_text("{}\n", encoding="utf-8")
        chmod_private(cookies_path, 0o600)

    result = {
        "ok": True,
        "account_file": str(account_path),
        "directory": str(directory),
        "mode_account_file": oct(stat.S_IMODE(account_path.stat().st_mode)),
        "mode_directory": oct(stat.S_IMODE(directory.stat().st_mode)),
        "secret_values_written": False,
        "warning": service_warning,
        "next_steps": [
            "Fill PASSWORD/TOTP_SECRET locally only after the account contract is approved.",
            "Run account_check.py before use.",
            "Do not commit or paste files under the private credential root.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
