#!/usr/bin/env python3
"""Redacted Hermes profile config/env parity probe.

Compares a named profile against the default Hermes home for operational parity.
Prints only redacted secrets. Intended for manual audits before patching profile drift.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML is required: {exc}")

SECRET_RE = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD|PASS|AUTH|COOKIE|CREDENTIAL|CLIENT_SECRET)", re.I)

OPERATIONAL_KEYS = [
    "model",
    "memory",
    "agent.disabled_toolsets",
    "platform_toolsets",
    "plugins",
    "known_plugin_toolsets",
    "delegation",
]
IDENTITY_KEYS = [
    "display.personality",
    "agent.personalities",
    "agent.system_prompt",
    "tts.edge.voice",
    "tts.mistral.voice_id",
    "tts.neutts.ref_audio",
    "tts.neutts.ref_text",
    "stt.provider",
    "stt.local.language",
]
ENV_FOCUS_SUBSTRINGS = [
    "EMAIL", "IMAP", "SMTP", "HINDSIGHT", "OPENROUTER", "OMNIROUTE", "SPOTIFY",
]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def parse_env(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, val = stripped.split("=", 1)
        values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def get_path(obj: Dict[str, Any], dotted: str, missing: Any = "<missing>") -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return missing
        cur = cur[part]
    return cur


def redact(key: str, value: Any) -> Any:
    if isinstance(value, dict):
        return {k: redact(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(key, v) for v in value]
    if SECRET_RE.search(key):
        if value in (None, "", "<missing>"):
            return value
        text = str(value)
        return f"[set len={len(text)} sha8={hashlib.sha256(text.encode()).hexdigest()[:8]}]"
    return value


def focused_env(default_env: Dict[str, str], profile_env: Dict[str, str]) -> list[dict[str, Any]]:
    keys = sorted(set(default_env) | set(profile_env))
    rows = []
    for key in keys:
        if not any(s in key.upper() for s in ENV_FOCUS_SUBSTRINGS):
            continue
        dv = default_env.get(key, "<missing>")
        pv = profile_env.get(key, "<missing>")
        rows.append({
            "key": key,
            "default": redact(key, dv),
            "profile": redact(key, pv),
            "same": dv == pv,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare default Hermes config/env with a named profile.")
    parser.add_argument("profile", help="Profile name, e.g. default")
    parser.add_argument("--home", default="~/.hermes/.hermes", help="Default Hermes home")
    args = parser.parse_args()

    home = Path(args.home).expanduser()
    profile_home = home / "profiles" / args.profile
    default_cfg = load_yaml(home / "config.yaml")
    profile_cfg = load_yaml(profile_home / "config.yaml")
    default_env = parse_env(home / ".env")
    profile_env = parse_env(profile_home / ".env")

    operational = []
    for key in OPERATIONAL_KEYS:
        dv = get_path(default_cfg, key)
        pv = get_path(profile_cfg, key)
        operational.append({"key": key, "same": dv == pv, "default": redact(key, dv), "profile": redact(key, pv)})

    identity = []
    for key in IDENTITY_KEYS:
        dv = get_path(default_cfg, key)
        pv = get_path(profile_cfg, key)
        identity.append({"key": key, "same": dv == pv, "default": redact(key, dv), "profile": redact(key, pv)})

    result = {
        "profile": args.profile,
        "paths": {
            "default_config": str(home / "config.yaml"),
            "profile_config": str(profile_home / "config.yaml"),
            "default_env": str(home / ".env"),
            "profile_env": str(profile_home / ".env"),
        },
        "operational_parity": operational,
        "identity_differences_expected": identity,
        "focused_env": focused_env(default_env, profile_env),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
