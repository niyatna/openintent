#!/usr/bin/env python3
"""Validate private account.txt shape and permissions without printing secrets."""
from __future__ import annotations

import argparse
import json
import stat
import sys
from pathlib import Path

SECRET_FIELDS = {"PASSWORD", "TOTP_SECRET", "TOKEN", "PRIVATE_KEY", "SEED_PHRASE", "BACKUP_CODE", "CLIENT_SECRET"}
DEFAULT_REQUIRED = ["ACCOUNT_ID", "OWNER", "SERVICE"]


def parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def mode(path: Path) -> str:
    return oct(stat.S_IMODE(path.stat().st_mode))


def mask(value: str) -> str:
    if not value:
        return ""
    if "@" in value:
        left, right = value.split("@", 1)
        return (left[:2] + "***@" + right) if len(left) > 2 else "***@" + right
    if len(value) <= 4:
        return "***"
    return value[:2] + "***" + value[-2:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate account.txt")
    parser.add_argument("--account-file", required=True)
    parser.add_argument("--require", action="append", default=[])
    args = parser.parse_args()

    path = Path(args.account_file)
    result = {
        "account_file": str(path),
        "exists": path.exists(),
        "mode": None,
        "ok": False,
        "missing": [],
        "warnings": [],
        "public_fields": {},
        "secret_fields_present": [],
    }
    if not path.exists():
        print(json.dumps(result, indent=2))
        return 1

    result["mode"] = mode(path)
    if result["mode"] != "0o600":
        result["warnings"].append(f"account file mode should be 0o600, got {result['mode']}")

    data = parse_env_file(path)
    required = list(dict.fromkeys(DEFAULT_REQUIRED + args.require))
    result["missing"] = [k for k in required if not data.get(k)]
    for key in ["ACCOUNT_ID", "OWNER", "SERVICE", "EMAIL", "USERNAME", "RECOVERY_EMAIL", "PHONE_LAST4", "COOKIES_FILE", "BACKUP_CODES_FILE"]:
        if key in data:
            result["public_fields"][key] = mask(data[key]) if key in {"EMAIL", "USERNAME", "RECOVERY_EMAIL"} else data[key]
    result["secret_fields_present"] = sorted([k for k in data if k in SECRET_FIELDS and bool(data.get(k))])
    result["ok"] = not result["missing"] and result["mode"] == "0o600"
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
