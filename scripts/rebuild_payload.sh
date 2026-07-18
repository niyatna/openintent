#!/usr/bin/env bash
# =============================================================================
# rebuild_payload.sh — Regenerate install.sh embedded payload
# =============================================================================
# Packs all git-tracked files into a base64 payload and embeds it in install.sh.
# Run this after any change to profiles/, scripts/, docker-compose.yml, or setup.sh.
# =============================================================================

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=== Rebuilding install.sh payload ===${NC}"

# ── 1. Collect tracked files ──────────────────────────────────────
echo -e "${YELLOW}1. Collecting git-tracked files...${NC}"

# Files that belong in the payload (what a fresh install needs)
PAYLOAD_DIRS=(
    profiles/
    scripts/
    docs/
)
PAYLOAD_FILES=(
    docker-compose.yml
    setup.sh
    AGENTS.md
    README.md
    LICENSE
    .gitignore
)

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

FILELIST="$TMPDIR/filelist.txt"
> "$FILELIST"

# Add individual files (tracked only)
for f in "${PAYLOAD_FILES[@]}"; do
    if git ls-files --error-unmatch "$f" &>/dev/null 2>&1; then
        echo "$f" >> "$FILELIST"
    elif [ -f "$f" ]; then
        echo "$f" >> "$FILELIST"
    fi
done

# Add directory contents (tracked only, exclude runtime/private .bak files)
for d in "${PAYLOAD_DIRS[@]}"; do
    git ls-files "$d" 2>/dev/null >> "$FILELIST" || true
done

# Deduplicate and sort
LC_ALL=C sort -u "$FILELIST" -o "$FILELIST"

FILE_COUNT=$(wc -l < "$FILELIST")
echo -e "  ${GREEN}${FILE_COUNT} files to pack${NC}"

# ── 2. Create tarball ─────────────────────────────────────────────
echo -e "${YELLOW}2. Creating payload tarball...${NC}"

TARBALL="$TMPDIR/payload.tar.gz"
LC_ALL=C tar cf - --mtime='2026-01-01' --sort=name --owner=0 --group=0 --numeric-owner -T "$FILELIST" | gzip -n > "$TARBALL"

TARBALL_SIZE=$(stat -c%s "$TARBALL" 2>/dev/null || stat -f%z "$TARBALL")
echo -e "  ${GREEN}Tarball: $(numfmt --to=iec "$TARBALL_SIZE" 2>/dev/null || echo "$TARBALL_SIZE bytes")${NC}"

# ── 3. Base64 encode ──────────────────────────────────────────────
echo -e "${YELLOW}3. Base64 encoding...${NC}"

B64="$TMPDIR/payload.b64"
base64 -w0 < "$TARBALL" > "$B64"

B64_SIZE=$(stat -c%s "$B64" 2>/dev/null || stat -f%z "$B64")
echo -e "  ${GREEN}Base64: $(numfmt --to=iec "$B64_SIZE" 2>/dev/null || echo "$B64_SIZE bytes")${NC}"

# ── 4. Splice into install.sh ─────────────────────────────────────
echo -e "${YELLOW}4. Embedding into install.sh...${NC}"

INSTALL="$DIR/install.sh"

if [ ! -f "$INSTALL" ]; then
    echo -e "${RED}ERROR: install.sh not found${NC}"
    exit 1
fi

# install.sh structure:
#   line 102: cat << 'EOF' | base64 -d > payload.tar.gz
#   line 103: <base64 data>
#   line 104: EOF
# We replace line 103 with the new payload

# Find the payload line (between the cat heredoc and EOF)
HEREDOC_LINE=$(grep -n "cat << 'EOF' | base64 -d" "$INSTALL" | head -1 | cut -d: -f1)
EOF_LINE=$(awk -v start="$HEREDOC_LINE" 'NR>start && /^EOF$/{print NR; exit}' "$INSTALL")

if [ -z "$HEREDOC_LINE" ] || [ -z "$EOF_LINE" ]; then
    echo -e "${RED}ERROR: Could not find payload markers in install.sh${NC}"
    echo "  Expected: cat << 'EOF' | base64 -d > payload.tar.gz ... EOF"
    exit 1
fi

PAYLOAD_LINE=$((HEREDOC_LINE + 1))
echo "  Heredoc start: line $HEREDOC_LINE"
echo "  Payload data:  line $PAYLOAD_LINE"
echo "  EOF marker:    line $EOF_LINE"

# Splice: head (lines 1..HEREDOC_LINE) + new payload + tail (lines EOF_LINE..end)
{
    head -n "$HEREDOC_LINE" "$INSTALL"
    cat "$B64"
    echo ""  # newline after base64
    tail -n +"$EOF_LINE" "$INSTALL"
} > "$TMPDIR/install_new.sh"

# Verify the new file parses
if bash -n "$TMPDIR/install_new.sh" 2>/dev/null; then
    cp "$TMPDIR/install_new.sh" "$INSTALL"
    chmod +x "$INSTALL"
    NEW_SIZE=$(stat -c%s "$INSTALL" 2>/dev/null || stat -f%z "$INSTALL")
    echo -e "  ${GREEN}install.sh updated: $(numfmt --to=iec "$NEW_SIZE" 2>/dev/null || echo "$NEW_SIZE bytes")${NC}"
else
    echo -e "${RED}ERROR: Generated install.sh has syntax errors — aborting${NC}"
    exit 1
fi

# ── 5. Verify round-trip ─────────────────────────────────────────
echo -e "${YELLOW}5. Verifying payload round-trip...${NC}"

VERIFY_DIR="$TMPDIR/verify"
mkdir -p "$VERIFY_DIR"
cd "$VERIFY_DIR"

# Extract the just-embedded payload
sed -n "$((HEREDOC_LINE + 1))p" "$INSTALL" | base64 -d > verify_payload.tar.gz
tar tzf verify_payload.tar.gz > /dev/null 2>&1

VERIFY_COUNT=$(tar tzf verify_payload.tar.gz | grep -v '/$' | wc -l)
echo -e "  ${GREEN}Round-trip OK: $VERIFY_COUNT files in payload${NC}"

cd "$DIR"

echo -e "\n${GREEN}=== Payload rebuilt successfully ===${NC}"
echo -e "  Files packed: $FILE_COUNT"
echo -e "  Run ${YELLOW}git diff --stat install.sh${NC} to review the change."
