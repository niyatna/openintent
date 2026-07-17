#!/usr/bin/env bash
# =============================================================================
# test_install.sh — Non-interactive dry-run of install.sh
# =============================================================================
# Exercises install.sh in CI by piping mock inputs via stdin.
# Validates: dependency detection, base64 payload extraction, .env generation,
# directory scaffolding, profile staging, and alignment with setup.sh structure.
#
# Ubuntu GH Actions runners have curl, tar, python3, docker pre-installed,
# so the auto-install branches are skipped (all deps return FOUND).
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

PASS=0
FAIL=0
WORKDIR=$(mktemp -d)

ok()   { PASS=$((PASS + 1)); echo "  ✓ $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  ✗ $1" >&2; }

cleanup() {
    rm -rf "$WORKDIR" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== install.sh Dry-Run Tests ==="
echo "  Workspace: $WORKDIR"

# ── Test 1: Syntax check ──────────────────────────────────────────
echo ""
echo "--- Test 1: Bash syntax check ---"
if bash -n install.sh 2>/dev/null; then
    ok "install.sh parses without syntax errors"
else
    fail "install.sh has syntax errors"
fi

# ── Test 2: Full non-interactive run ──────────────────────────────
echo ""
echo "--- Test 2: Piped non-interactive execution ---"

# install.sh expects 3 prompts (when .env doesn't exist):
#   1. Target directory path (default: ./openintent)
#   2. OpenRouter API Key
#   3. Discord Bot Token
printf '%s\n' "$WORKDIR/test-install" "sk-or-ci-test-dummy-key" "MTEyMjMzNDQ1NTY2Nzc.ci.dummy-discord-token" \
    | bash install.sh

INSTALL_DIR="$WORKDIR/test-install"

if [ -d "$INSTALL_DIR" ]; then
    ok "Install directory created"
else
    fail "Install directory not created at $INSTALL_DIR"
    echo "=== Results: $PASS passed, $FAIL failed ==="
    exit 1
fi

# ── Test 3: Base64 payload extracted ──────────────────────────────
echo ""
echo "--- Test 3: Payload extraction ---"

# payload.tar.gz should be extracted and removed; check for extracted content
# The payload contains: profiles/, scripts/, docker-compose.yml, setup.sh
for expected in docker-compose.yml setup.sh scripts/verify.sh scripts/discord_setup.py scripts/init_9router_db.py; do
    if [ -f "$INSTALL_DIR/$expected" ]; then
        ok "Extracted: $expected"
    else
        fail "Missing after extraction: $expected"
    fi
done

# payload.tar.gz itself should have been cleaned up or still present
# (install.sh may or may not remove it — just check extraction worked)

# ── Test 4: .env generated ────────────────────────────────────────
echo ""
echo "--- Test 4: .env generation ---"

if [ -f "$INSTALL_DIR/.env" ]; then
    ok ".env file created"
else
    fail ".env file not created"
fi

if grep -q "sk-or-ci-test-dummy-key" "$INSTALL_DIR/.env" 2>/dev/null; then
    ok ".env contains OpenRouter key"
else
    fail ".env missing OpenRouter key"
fi

if grep -q "dummy-discord-token" "$INSTALL_DIR/.env" 2>/dev/null; then
    ok ".env contains Discord token"
else
    fail ".env missing Discord token"
fi

# ── Test 5: Directory structure matches setup.sh ──────────────────
echo ""
echo "--- Test 5: Directory structure (aligned with setup.sh) ---"

for dir in data/hermes data/hermes/profiles/corporate-agent data/hermes/profiles/public-agent; do
    if [ -d "$INSTALL_DIR/$dir" ]; then
        ok "Directory: $dir"
    else
        fail "Missing directory: $dir"
    fi
done

# ── Test 6: Profile staging (default → data/hermes/) ──────────────
echo ""
echo "--- Test 6: Profile staging ---"

if [ -f "$INSTALL_DIR/data/hermes/config.yaml" ]; then
    ok "Default profile config.yaml staged to data/hermes/"
else
    fail "Default profile config.yaml not staged"
fi

for profile in corporate-agent public-agent; do
    if [ -f "$INSTALL_DIR/data/hermes/profiles/$profile/config.yaml" ]; then
        ok "$profile config.yaml staged"
    else
        fail "$profile config.yaml not staged"
    fi
done

# ── Test 7: .env bound to profiles ────────────────────────────────
echo ""
echo "--- Test 7: .env bound to profile directories ---"

for env_path in data/hermes/.env data/hermes/profiles/corporate-agent/.env data/hermes/profiles/public-agent/.env; do
    if [ -f "$INSTALL_DIR/$env_path" ]; then
        ok "$env_path bound"
    else
        fail "$env_path not bound"
    fi
done

# ── Test 8: discord_setup.py copied ───────────────────────────────
echo ""
echo "--- Test 8: Script endpoints ---"

if [ -f "$INSTALL_DIR/data/hermes/discord_setup.py" ]; then
    ok "discord_setup.py copied to data/hermes/"
else
    fail "discord_setup.py not copied"
fi

# ── Test 9: Script permissions ────────────────────────────────────
echo ""
echo "--- Test 9: Executable permissions ---"

for script in scripts/verify.sh scripts/discord_setup.py scripts/init_9router_db.py; do
    if [ -x "$INSTALL_DIR/$script" ]; then
        ok "$script is executable"
    else
        fail "$script is not executable"
    fi
done

# ── Test 10: No stale agentic-company references ─────────────────
echo ""
echo "--- Test 10: No stale agentic-company references ---"

if grep -rq "agentic-company" "$INSTALL_DIR/install.sh" 2>/dev/null; then
    fail "install.sh still references agentic-company"
else
    ok "No agentic-company references in install.sh"
fi

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
