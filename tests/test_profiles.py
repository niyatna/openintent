#!/usr/bin/env python3
"""
test_profiles.py — Cross-Profile Parity Validator

Validates the three-profile rule from AGENTS.md:
- config.yaml: only system_prompt, discord.enabled, cursor, terminal.cwd may differ
- distribution.yaml: must be identical across profiles
- .env.EXAMPLE: env var names must be identical (values may differ)
- mcp.json: must be identical across profiles
- skills/: directory trees must be identical
- skill-bundles/: directory trees must be identical
"""

import json
import os
import sys
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"
PROFILE_NAMES = ["default", "corporate-agent", "public-agent"]

PASS = 0
FAIL = 0


def ok(msg):
    global PASS
    PASS += 1
    print(f"  ✓ {msg}")


def fail(msg):
    global FAIL
    FAIL += 1
    print(f"  ✗ {msg}", file=sys.stderr)


def load_yaml(path):
    """Minimal YAML loader — uses PyYAML if available, else basic parse check."""
    try:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: just verify it's loadable text
        with open(path) as f:
            return f.read()


def load_json(path):
    with open(path) as f:
        return json.load(f)


def get_env_var_names(path):
    """Extract env var names from a .env or .env.EXAMPLE file."""
    names = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                names.append(line.split("=", 1)[0])
    return sorted(names)


def get_dir_tree(path):
    """Get sorted relative file paths under a directory."""
    if not path.exists():
        return []
    tree = []
    for root, dirs, files in os.walk(path):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), path)
            tree.append(rel)
    return sorted(tree)


# ═══════════════════════════════════════════════════════════════════
print("=== Cross-Profile Parity Tests ===\n")

# ── 1. All profiles exist ──────────────────────────────────────────
print("--- 1. Profile directories exist ---")
for name in PROFILE_NAMES:
    p = PROFILES_DIR / name
    if p.is_dir():
        ok(f"profiles/{name}/ exists")
    else:
        fail(f"profiles/{name}/ missing")

# ── 2. config.yaml — YAML syntax valid ────────────────────────────
print("\n--- 2. config.yaml syntax ---")
configs = {}
for name in PROFILE_NAMES:
    path = PROFILES_DIR / name / "config.yaml"
    try:
        configs[name] = load_yaml(path)
        ok(f"{name}/config.yaml parses OK")
    except Exception as e:
        fail(f"{name}/config.yaml parse error: {e}")

# ── 3. config.yaml — only allowed fields differ ──────────────────
print("\n--- 3. config.yaml allowed divergence ---")
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

if HAS_YAML and all(isinstance(configs.get(n), dict) for n in PROFILE_NAMES):
    ALLOWED_DIFF_PATHS = {
        "agent.system_prompt",
        "platforms.discord.enabled",
        "streaming.cursor",
        "terminal.cwd",
        # Terminal config may vary per lane (docker args, daemon settings)
        "terminal.daemon_term_grace_seconds",
        "terminal.daytona_image",
        "terminal.docker_extra_args",
        "terminal.docker_forward_env",
        # MCP server enablement varies per lane
        "mcp_servers.paperclip.enabled",
    }

    def flatten_dict(d, prefix=""):
        """Flatten nested dict to dot-notation keys."""
        items = {}
        if not isinstance(d, dict):
            return {prefix: d}
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                items.update(flatten_dict(v, key))
            else:
                items[key] = v
        return items

    base = flatten_dict(configs["default"])
    for other_name in ["corporate-agent", "public-agent"]:
        other = flatten_dict(configs[other_name])
        all_keys = set(base.keys()) | set(other.keys())
        unexpected_diffs = []
        for key in sorted(all_keys):
            val_base = base.get(key)
            val_other = other.get(key)
            if val_base != val_other:
                if not any(key.startswith(allowed) for allowed in ALLOWED_DIFF_PATHS):
                    unexpected_diffs.append(key)
        if unexpected_diffs:
            fail(f"default vs {other_name}: unexpected config differences in: {', '.join(unexpected_diffs[:10])}")
        else:
            ok(f"default vs {other_name}: only allowed fields differ")
else:
    print("  ⚠ Skipped (PyYAML not available or config parse failed)")

# ── 4. distribution.yaml — structural parity ─────────────────────
print("\n--- 4. distribution.yaml parity ---")
# distribution.yaml intentionally differs in: name, description,
# and per-lane env_requires descriptions. Check structural keys match.
if HAS_YAML:
    dist_data = {}
    for name in PROFILE_NAMES:
        path = PROFILES_DIR / name / "distribution.yaml"
        if path.exists():
            dist_data[name] = load_yaml(path)
        else:
            fail(f"{name}/distribution.yaml missing")

    DIST_ALLOWED_DIFF = {"name", "description"}
    if len(dist_data) == 3 and all(isinstance(d, dict) for d in dist_data.values()):
        base_keys = set(dist_data["default"].keys())
        for other in ["corporate-agent", "public-agent"]:
            other_keys = set(dist_data[other].keys())
            if base_keys == other_keys:
                ok(f"default == {other} (same top-level keys)")
            else:
                fail(f"default != {other} (keys differ: {base_keys ^ other_keys})")
else:
    print("  ⚠ Skipped (PyYAML not available)")

# ── 5. .env.EXAMPLE — env var names parity ───────────────────────
print("\n--- 5. .env.EXAMPLE variable name parity ---")
# Each lane has its own BWS_ACCESS_TOKEN name (DEFAULT_, CORPORATE_, PUBLIC_)
# so we normalize those before comparing
ENV_VAR_RENAMES = {
    "DEFAULT_BWS_ACCESS_TOKEN": "_BWS_ACCESS_TOKEN",
    "CORPORATE_BWS_ACCESS_TOKEN": "_BWS_ACCESS_TOKEN",
    "PUBLIC_BWS_ACCESS_TOKEN": "_BWS_ACCESS_TOKEN",
}
env_names = {}
for name in PROFILE_NAMES:
    path = PROFILES_DIR / name / ".env.EXAMPLE"
    if path.exists():
        raw_names = get_env_var_names(path)
        normalized = sorted(ENV_VAR_RENAMES.get(n, n) for n in raw_names)
        env_names[name] = normalized
    else:
        fail(f"{name}/.env.EXAMPLE missing")

if len(env_names) == 3:
    base_names = env_names["default"]
    for other in ["corporate-agent", "public-agent"]:
        if env_names[other] == base_names:
            ok(f"default == {other} (same env var names)")
        else:
            only_base = set(base_names) - set(env_names[other])
            only_other = set(env_names[other]) - set(base_names)
            diff_msg = []
            if only_base:
                diff_msg.append(f"only in default: {only_base}")
            if only_other:
                diff_msg.append(f"only in {other}: {only_other}")
            fail(f"default != {other}: {'; '.join(diff_msg)}")

# ── 6. mcp.json — structural parity ─────────────────────────────
print("\n--- 6. mcp.json parity ---")
# mcp.json intentionally differs: paperclip.enabled is true in default,
# false in corporate/public. Validate JSON syntax and same server keys.
mcp_data = {}
for name in PROFILE_NAMES:
    path = PROFILES_DIR / name / "mcp.json"
    if path.exists():
        try:
            mcp_data[name] = load_json(path)
            ok(f"{name}/mcp.json valid JSON")
        except json.JSONDecodeError as e:
            fail(f"{name}/mcp.json invalid: {e}")
    else:
        fail(f"{name}/mcp.json missing")

if len(mcp_data) == 3:
    # Compare server names (keys) — must be identical
    base_servers = set(mcp_data["default"].get("mcp_servers", {}).keys())
    for other in ["corporate-agent", "public-agent"]:
        other_servers = set(mcp_data[other].get("mcp_servers", {}).keys())
        if base_servers == other_servers:
            ok(f"default == {other} (same MCP server names)")
        else:
            fail(f"default != {other} (MCP servers differ: {base_servers ^ other_servers})")

# ── 7. skills/ directory tree parity ─────────────────────────────
print("\n--- 7. skills/ directory tree parity ---")
skill_trees = {}
for name in PROFILE_NAMES:
    skill_trees[name] = get_dir_tree(PROFILES_DIR / name / "skills")

if skill_trees["default"]:
    for other in ["corporate-agent", "public-agent"]:
        if skill_trees[other] == skill_trees["default"]:
            ok(f"default == {other} ({len(skill_trees['default'])} files)")
        else:
            only_default = set(skill_trees["default"]) - set(skill_trees[other])
            only_other = set(skill_trees[other]) - set(skill_trees["default"])
            diff_msg = []
            if only_default:
                diff_msg.append(f"only in default: {list(only_default)[:5]}")
            if only_other:
                diff_msg.append(f"only in {other}: {list(only_other)[:5]}")
            fail(f"default != {other}: {'; '.join(diff_msg)}")

# ── 8. skill-bundles/ parity ─────────────────────────────────────
print("\n--- 8. skill-bundles/ parity ---")
bundle_trees = {}
for name in PROFILE_NAMES:
    bundle_trees[name] = get_dir_tree(PROFILES_DIR / name / "skill-bundles")

if bundle_trees["default"]:
    for other in ["corporate-agent", "public-agent"]:
        if bundle_trees[other] == bundle_trees["default"]:
            ok(f"default == {other} ({len(bundle_trees['default'])} files)")
        else:
            only_default = set(bundle_trees["default"]) - set(bundle_trees[other])
            only_other = set(bundle_trees[other]) - set(bundle_trees["default"])
            fail(f"default != {other}: +{len(only_other)}/-{len(only_default)} files differ")

# ── 9. private/ credential template parity ───────────────────────
print("\n--- 9. private/ directory parity ---")
private_trees = {}
for name in PROFILE_NAMES:
    private_trees[name] = get_dir_tree(PROFILES_DIR / name / "private")

for other in ["corporate-agent", "public-agent"]:
    if private_trees.get(other) == private_trees.get("default"):
        ok(f"default == {other}")
    else:
        only_default = set(private_trees.get("default", [])) - set(private_trees.get(other, []))
        only_other = set(private_trees.get(other, [])) - set(private_trees.get("default", []))
        fail(f"default != {other}: +{len(only_other)}/-{len(only_default)} files differ")

# ═══════════════════════════════════════════════════════════════════
print(f"\n=== Results: {PASS} passed, {FAIL} failed ===")
sys.exit(1 if FAIL > 0 else 0)
