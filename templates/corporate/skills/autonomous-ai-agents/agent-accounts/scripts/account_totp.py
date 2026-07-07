#!/usr/bin/env python3
"""Generate a TOTP code from a private account.txt without printing secrets."""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import struct
import sys
import time
from pathlib import Path

SECRET_KEYS = {"PASSWORD", "TOTP_SECRET", "TOKEN", "PRIVATE_KEY", "SEED_PHRASE", "BACKUP_CODE"}


def parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def hotp(secret: str, counter: int, digits: int = 6) -> str:
    normalized = "".join(secret.split()).upper()
    padding = "=" * ((8 - len(normalized) % 8) % 8)
    key = base64.b32decode(normalized + padding, casefold=True)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code_int = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(code_int % (10 ** digits)).zfill(digits)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TOTP from account.txt")
    parser.add_argument("--account-file", required=True)
    parser.add_argument("--period", type=int, default=30)
    parser.add_argument("--digits", type=int, default=6)
    args = parser.parse_args()

    path = Path(args.account_file)
    if not path.exists():
        print(f"ERROR: missing account file: {path}", file=sys.stderr)
        return 1
    data = parse_env_file(path)
    secret = data.get("TOTP_SECRET")
    if not secret:
        print("ERROR: TOTP_SECRET missing", file=sys.stderr)
        return 1
    now = int(time.time())
    step = now // args.period
    code = hotp(secret, step, digits=args.digits)
    remaining = args.period - (now % args.period)
    owner = data.get("OWNER", "")
    service = data.get("SERVICE", "")
    account_id = data.get("ACCOUNT_ID", "")
    print(f"otp={code}")
    print(f"valid_for_seconds={remaining}")
    print(f"account_id={account_id}")
    print(f"owner={owner}")
    print(f"service={service}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
