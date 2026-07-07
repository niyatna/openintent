#!/usr/bin/env python3
"""Audit Keiya/Galyarder access-autonomy hardening invariants.

This checks the security maturity-loop implementation surfaces:
SOUL contracts, non-secret credential registry, behavior QA docs, permissions,
and config safety settings. It does not print secret values.
"""
from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

import yaml

HOME = Path("/home/galyarder/.hermes")
REPORT = HOME / "reports/agent-os/access-hardening-latest.json"
REPORT.parent.mkdir(parents=True, exist_ok=True)

errors: list[str] = []
warnings: list[str] = []
checks: list[dict[str, Any]] = []


def record(name: str, ok: bool, detail: str = "", *, warn: bool = False) -> None:
    status = "warn" if warn else ("pass" if ok else "fail")
    checks.append({"name": name, "status": status, "detail": detail})
    if warn:
        warnings.append(name + (f": {detail}" if detail else ""))
    elif not ok:
        errors.append(name + (f": {detail}" if detail else ""))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def require_file(path: Path) -> bool:
    ok = path.exists() and path.is_file()
    record(f"file exists: {path}", ok)
    return ok


def require_dir(path: Path) -> bool:
    ok = path.exists() and path.is_dir()
    record(f"dir exists: {path}", ok)
    return ok


def require_text(path: Path, phrases: list[str]) -> None:
    if not require_file(path):
        return
    text = read(path).lower()
    missing = [p for p in phrases if p.lower() not in text]
    record(f"text invariants: {path}", not missing, "missing: " + ", ".join(missing) if missing else "PASS")


def mode(path: Path) -> str | None:
    if not path.exists():
        return None
    return oct(stat.S_IMODE(path.stat().st_mode))


def require_mode(path: Path, expected: str) -> None:
    actual = mode(path)
    record(f"mode {expected}: {path}", actual == expected, f"actual={actual}")


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text())
        return data or {}
    except Exception as exc:  # pragma: no cover - diagnostic path
        record(f"yaml parse: {path}", False, repr(exc))
        return {}


required_contract_phrases = [
    "## Access Ownership Matrix",
    "## Autonomy Matrix",
    "## Credential Reference Rules",
    "## External/Public Action Confirmation Thresholds",
    "## Resource Management: start → use → stop",
    "## Autonomous Login Boundary",
    "## Behavior QA Contract",
    "## Default Disposition",
    "/home/galyarder/.hermes/private/credentials/access-registry.yaml",
]

require_text(HOME / "SOUL.md", required_contract_phrases)
require_text(HOME / "profiles/galyarder/SOUL.md", required_contract_phrases)

credential_dir = HOME / "private/credentials"
registry = credential_dir / "access-registry.yaml"
readme = credential_dir / "README.md"
require_dir(HOME / "private")
require_dir(credential_dir)
require_file(readme)
require_file(registry)
require_mode(HOME / "private", "0o700")
require_mode(credential_dir, "0o700")
require_mode(readme, "0o600")
require_mode(registry, "0o600")
require_mode(HOME / "google_token.json", "0o600")
require_mode(Path("/home/galyarder/.config/gws/client_secret.json"), "0o600")

registry_data = load_yaml(registry) if registry.exists() else {}
accesses = registry_data.get("accesses") if isinstance(registry_data, dict) else None
required_accesses = {
    "discord_keiya",
    "discord_galyarder",
    "google_workspace",
    "obsidian_keiya",
    "obsidian_galyarder",
    "terminal_files",
    "browser_web",
    "profile_distribution_repos",
    "mcp_business_tools",
    "cron_automation",
    "social_wallet_finance",
    "agent_owned_google_keiya",
    "agent_owned_google_galyarder",
    "agent_owned_github_keiya",
    "agent_owned_github_galyarder",
    "agent_owned_x_keiya",
    "agent_owned_x_galyarder",
    "agent_owned_wallet_keiya",
    "agent_owned_wallet_galyarder",
}
if isinstance(accesses, dict):
    missing = sorted(required_accesses - set(accesses))
    record("credential registry required domains", not missing, "missing: " + ", ".join(missing) if missing else "PASS")
    for name, entry in sorted(accesses.items()):
        if not isinstance(entry, dict):
            record(f"registry entry shape: {name}", False, "not mapping")
            continue
        for key in ["owner_status", "credential_reference", "capabilities", "fully_autonomous", "autonomous_plus_log", "requires_confirmation", "verification", "recovery"]:
            record(f"registry {name}.{key}", key in entry, "missing" if key not in entry else "PASS")
else:
    record("credential registry accesses mapping", False, "missing or invalid")

# Secret leakage heuristic for registry/docs: catches obvious assignment-like secrets,
# not env var names. Values should not look like real bearer/token/password material.
secret_like = []
for path in [registry, readme]:
    if not path.exists():
        continue
    for idx, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        lower = line.lower().strip()
        if any(k in lower for k in ["password:", "token:", "api_key:", "private_key:", "totp_secret:", "backup_code:", "cookie:"]):
            # allow documentation labels when value is blank/list/path-only? In this registry,
            # these labels should not appear as scalar secret fields at all.
            secret_like.append(f"{path}:{idx}:{line[:120]}")
record("registry/docs no obvious secret scalar fields", not secret_like, "\n".join(secret_like[:10]) if secret_like else "PASS")

behavior_dir = HOME / "behavior-tests"
require_dir(behavior_dir)
required_behavior_files = [
    "README.md",
    "keiya-behavior-tests.md",
    "galyarder-behavior-tests.md",
    "access-boundary-tests.md",
    "relay-tests.md",
    "access-rollout-runbook.md",
    "config-hardening-audit.md",
]
for fname in required_behavior_files:
    require_file(behavior_dir / fname)

require_text(behavior_dir / "access-boundary-tests.md", ["Send external email", "Force push", "Credential entry/login recovery", "Validate agent-owned account skeletons", "Populate agent-owned credentials", "Pass criteria"])
require_text(behavior_dir / "relay-tests.md", ["raw mention", "split chunks", "no ping-pong", "side-effect verification"])
require_text(behavior_dir / "access-rollout-runbook.md", ["profile → one access → behavior contract", "read-only test", "safe write test", "Autonomous login gate", "Agent-owned account skeleton gate"])

account_checker = HOME / "skills/autonomous-ai-agents/agent-accounts/scripts/account_check.py"
require_file(account_checker)
agent_root = credential_dir / "agents"
require_dir(agent_root)
require_mode(agent_root, "0o700")
for owner in ["keiya", "galyarder"]:
    for service in ["google", "github", "x", "wallet"]:
        service_dir = agent_root / owner / service
        account_file = service_dir / "account.txt"
        require_dir(service_dir)
        require_mode(service_dir, "0o700")
        require_file(account_file)
        require_mode(account_file, "0o600")
        if account_file.exists():
            account_data = read(account_file)
            for phrase in ["ACCOUNT_ID=", "OWNER=", "SERVICE=", "NOTES=dedicated agent-owned account; secrets are local-only"]:
                record(f"account skeleton {owner}/{service} has {phrase}", phrase in account_data, "PASS" if phrase in account_data else "missing")
            fields = {}
            for line in account_data.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                fields[key.strip()] = value.strip().strip('"').strip("'")
            secret_values = {key: fields.get(key, "") for key in ["PASSWORD", "TOTP_SECRET", "TOKEN", "PRIVATE_KEY", "SEED_PHRASE", "BACKUP_CODE"] if fields.get(key, "")}
            operational_status = fields.get("STATUS", "")
            # Empty planned skeletons must not contain populated secrets. Once Galih explicitly promotes
            # an account to operational agent-owned access, the private credential file may contain
            # password/TOTP material; the guard then verifies shape/permissions without printing values.
            credential_status_prefixes = (
                "credential-stored",
                "login-active",
                "github-login-active",
                "github-2fa-enabled",
                "github-signup",
                "x-login-active",
                "x-login-not-authenticated",
                "x-login-blocked-",
                "wallet-keystore",
                "wallet-policy-defined",
            )
            if operational_status.startswith(credential_status_prefixes):
                allowed_secret_keys = {"PASSWORD", "TOTP_SECRET"}
                disallowed_secret_values = {key: value for key, value in secret_values.items() if key not in allowed_secret_keys}
                record(f"operational account {owner}/{service} has no disallowed secret fields", not disallowed_secret_values, "present=" + ",".join(sorted(disallowed_secret_values)) if disallowed_secret_values else "PASS")
                if service == "google":
                    record(f"operational account {owner}/{service} has PASSWORD/TOTP for autonomous recovery", bool(fields.get("PASSWORD")) and bool(fields.get("TOTP_SECRET")), "PASS" if fields.get("PASSWORD") and fields.get("TOTP_SECRET") else "missing")
                elif service in {"github", "x"}:
                    record(f"operational account {owner}/{service} has PASSWORD for credentialed login", bool(fields.get("PASSWORD")), "PASS" if fields.get("PASSWORD") else "missing")
                    totp_status = fields.get("TOTP_STATUS", "")
                    pending_or_configured = bool(fields.get("TOTP_SECRET")) or totp_status in {"pending-setup", "not-configured", "github-totp-verify-failed"}
                    record(f"operational account {owner}/{service} TOTP state tracked", pending_or_configured, "PASS" if pending_or_configured else f"totp_status={totp_status or 'missing'}")
            else:
                record(f"account skeleton {owner}/{service} has no populated secret fields", not secret_values, "present=" + ",".join(sorted(secret_values)) if secret_values else "PASS")
        for optional in [service_dir / "backup-codes.txt", service_dir / "cookies.json", service_dir / "token.env"]:
            if optional.exists():
                require_mode(optional, "0o600")

# Portable profile-distribution artifacts: behavior tests are safe, but the private
# credential registry is deliberately local-only unless encrypted/explicitly approved.
for dist_label, dist_path in [
    ("keiya", HOME / "profile-distributions/keiya-profile"),
    ("galyarder", HOME / "profile-distributions/galyarder-profile"),
]:
    if dist_path.exists():
        require_file(dist_path / "RESTORE.md")
        restore_text = read(dist_path / "RESTORE.md") if (dist_path / "RESTORE.md").exists() else ""
        record(f"{dist_label} distribution documents credential-registry exclusion", "private credential registry" in restore_text.lower(), "PASS" if "private credential registry" in restore_text.lower() else "missing exclusion note")
        private_candidates = [p for p in dist_path.rglob("*") if "private/credentials" in str(p)]
        record(f"{dist_label} distribution excludes private credential registry", not private_candidates, "\n".join(map(str, private_candidates[:10])) if private_candidates else "PASS")
        require_dir(dist_path / "behavior-tests")
        for fname in required_behavior_files:
            require_file(dist_path / "behavior-tests" / fname)
        dist_yaml = load_yaml(dist_path / "distribution.yaml") if (dist_path / "distribution.yaml").exists() else {}
        owned = dist_yaml.get("distribution_owned") or []
        record(f"{dist_label} distribution owns behavior-tests", "behavior-tests/" in owned, str(owned))
        record(f"{dist_label} distribution excludes private credential registry from owned paths", not any("private" in str(x) or "credentials" in str(x) for x in owned), str(owned))

# Config safety checks.
for label, cfg_path in [("default", HOME / "config.yaml"), ("galyarder", HOME / "profiles/galyarder/config.yaml")]:
    cfg = load_yaml(cfg_path)
    record(f"{label} fallback_providers present", bool(cfg.get("fallback_providers")), "count=" + str(len(cfg.get("fallback_providers") or [])))
    approvals = cfg.get("approvals") or {}
    record(f"{label} approvals.mcp_reload_confirm true", approvals.get("mcp_reload_confirm") is True, f"actual={approvals.get('mcp_reload_confirm')}")
    record(f"{label} approvals.cron_mode deny", approvals.get("cron_mode") == "deny", f"actual={approvals.get('cron_mode')}")
    browser = cfg.get("browser") or {}
    record(f"{label} browser.record_sessions false", browser.get("record_sessions") is False, f"actual={browser.get('record_sessions')}")
    security = cfg.get("security") or {}
    record(f"{label} security.redact_secrets true", security.get("redact_secrets") is True, f"actual={security.get('redact_secrets')}")
    record(f"{label} hooks_auto_accept false", cfg.get("hooks_auto_accept") is False, f"actual={cfg.get('hooks_auto_accept')}")
    skills = cfg.get("skills") or {}
    record(f"{label} skills.guard_agent_created true", skills.get("guard_agent_created") is True, f"actual={skills.get('guard_agent_created')}")
    delegation = cfg.get("delegation") or {}
    record(f"{label} delegation bounded concurrency", isinstance(delegation.get("max_concurrent_children"), int) and delegation.get("max_concurrent_children") <= 3, f"actual={delegation.get('max_concurrent_children')}")
    record(f"{label} delegation depth bounded", isinstance(delegation.get("max_spawn_depth"), int) and delegation.get("max_spawn_depth") <= 3, f"actual={delegation.get('max_spawn_depth')}")
    code_exec = cfg.get("code_execution") or {}
    record(f"{label} code_execution timeout bounded", isinstance(code_exec.get("timeout"), int) and code_exec.get("timeout") <= 300, f"actual={code_exec.get('timeout')}")
    tools = (cfg.get("platform_toolsets") or {}).get("discord") or []
    record(f"{label} discord toolset enabled", "discord" in tools, "PASS" if "discord" in tools else str(tools))
    record(f"{label} discord_admin disabled", "discord_admin" not in tools, "PASS" if "discord_admin" not in tools else str(tools))
    memory = cfg.get("memory") or {}
    record(f"{label} memory provider hindsight", memory.get("provider") == "hindsight", f"actual={memory.get('provider')}")
    # Keiya currently uses yolo + domain contract; Galyarder manual. Warn if changed unexpectedly.
    expected_mode = "yolo" if label == "default" else "manual"
    record(f"{label} approval mode expected", approvals.get("mode") == expected_mode, f"actual={approvals.get('mode')} expected={expected_mode}", warn=approvals.get("mode") != expected_mode)

status = "fail" if errors else "pass"
report = {"status": status, "errors": errors, "warnings": warnings, "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
print("REPORT", REPORT)
raise SystemExit(1 if errors else 0)
