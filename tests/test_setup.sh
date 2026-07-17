#!/usr/bin/env bash
# =============================================================================
# test_setup.sh — Non-interactive dry-run of setup.sh
# =============================================================================
# Exercises setup.sh in CI by piping mock credentials via stdin.
# Validates: dependency checks, .env generation, directory scaffolding,
# profile staging, and file permissions.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

PASS=0
FAIL=0

ok()   { PASS=$((PASS + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  ✗ $1" >&2; }

echo "=== setup.sh Dry-Run Tests ==="

# ── Test 1: Syntax check ──────────────────────────────────────────
echo ""
echo "--- Test 1: Bash syntax check ---"
if bash -n setup.sh 2>/dev/null; then
    ok "setup.sh parses without syntax errors"
else
    fail "setup.sh has syntax errors"
fi

# ── Test 2: Non-interactive .env generation ───────────────────────
echo ""
echo "--- Test 2: .env generation with piped input ---"

# Clean any previous state
rm -rf data/ .env 2>/dev/null || true

# Pipe mock credentials: OpenRouter key + Discord token
# setup.sh expects two `read -rp` prompts in sequence
printf 'sk-or-test-dummy-key-12345\nMTEyMjMzNDQ1NTY2Nzc.test.dummy-discord-token\n' | bash setup.sh

if [ -f .env ]; then
    ok ".env file created"
else
    fail ".env file not created"
fi

# Verify .env contains the mock values
if grep -q "sk-or-test-dummy-key-12345" .env 2>/dev/null; then
    ok ".env contains OpenRouter key"
else
    fail ".env missing OpenRouter key"
fi

if grep -q "dummy-discord-token" .env 2>/dev/null; then
    ok ".env contains Discord token"
else
    fail ".env missing Discord token"
fi

# Verify auto-generated secrets exist (not empty)
for secret in BETTER_AUTH_SECRET JWT_SECRET INITIAL_PASSWORD DASHBOARD_PASSWORD DASHBOARD_SECRET; do
    val=$(grep "^${secret}=" .env | cut -d= -f2-)
    if [ -n "$val" ] && [ "$val" != "" ]; then
        ok ".env has generated $secret"
    else
        fail ".env missing or empty $secret"
    fi
done

# ── Test 3: Directory structure scaffolding ───────────────────────
echo ""
echo "--- Test 3: Directory structure ---"

for dir in data/hermes data/hermes/profiles/corporate-agent data/hermes/profiles/public-agent; do
    if [ -d "$dir" ]; then
        ok "Directory $dir exists"
    else
        fail "Directory $dir missing"
    fi
done

# ── Test 4: Profile staging ───────────────────────────────────────
echo ""
echo "--- Test 4: Profile distribution staging ---"

# Check that config.yaml was copied to data/hermes/
if [ -f data/hermes/config.yaml ]; then
    ok "Default profile config.yaml staged"
else
    fail "Default profile config.yaml not staged"
fi

if [ -f data/hermes/profiles/corporate-agent/config.yaml ]; then
    ok "Corporate profile config.yaml staged"
else
    fail "Corporate profile config.yaml not staged"
fi

if [ -f data/hermes/profiles/public-agent/config.yaml ]; then
    ok "Public profile config.yaml staged"
else
    fail "Public profile config.yaml not staged"
fi

# Check .env was bound to each profile
for profile_env in data/hermes/.env data/hermes/profiles/corporate-agent/.env data/hermes/profiles/public-agent/.env; do
    if [ -f "$profile_env" ]; then
        ok "$profile_env bound"
    else
        fail "$profile_env not bound"
    fi
done

# Check discord_setup.py was copied
if [ -f data/hermes/discord_setup.py ]; then
    ok "discord_setup.py copied to data/hermes/"
else
    fail "discord_setup.py not copied"
fi

# ── Test 5: Script permissions ────────────────────────────────────
echo ""
echo "--- Test 5: Script permissions ---"

for script in scripts/verify.sh scripts/discord_setup.py scripts/init_9router_db.py; do
    if [ -x "$script" ]; then
        ok "$script is executable"
    else
        fail "$script is not executable"
    fi
done

# ── Test 6: Idempotency — running again should skip .env ──────────
echo ""
echo "--- Test 6: Idempotency (second run skips .env) ---"

# Capture .env checksum before
CHECKSUM_BEFORE=$(sha256sum .env | cut -d' ' -f1)

# Run again with empty stdin (no prompts should fire since .env exists)
echo "" | bash setup.sh 2>/dev/null || true

CHECKSUM_AFTER=$(sha256sum .env | cut -d' ' -f1)
if [ "$CHECKSUM_BEFORE" = "$CHECKSUM_AFTER" ]; then
    ok "Idempotent: .env unchanged on second run"
else
    fail "Idempotent: .env was modified on second run"
fi

# ── Cleanup ───────────────────────────────────────────────────────
rm -rf data/ .env 2>/dev/null || true

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
