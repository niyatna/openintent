#!/usr/bin/env python3
# =============================================================================
# OpenIntent Kit - Interactive Provisioner
# =============================================================================
# Idempotent bootstrap installer for the OpenIntent multi-agent stack.
# Checks dependencies, provisions credentials, and sets up configurations.
# =============================================================================

set -euo pipefail

DIR="/home/galyarder/projects/openintent"
cd "$DIR"

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}     OpenIntent Kit Bootstrap Provisioner      ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Check base requirements
check_dep() {
    local cmd=$1
    echo -n "Checking prerequisite system dependency: $cmd... "
    if command -v "$cmd" &>/dev/null; then
        echo -e "${GREEN}FOUND${NC}"
    else
        echo -e "${RED}MISSING${NC} (Please install $cmd first)"
        exit 1
    fi
}

check_dep "docker"
check_dep "git"
check_dep "curl"
check_dep "python3"

# 1. Environment Configurations Setup
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Provisioning environment configuration credentials (.env)...${NC}"
    
    # Prompt for OpenRouter Key (Required)
    while true; do
        read -rp "Enter OpenRouter API Key (Required): " OPENROUTER_KEY
        if [ -n "$OPENROUTER_KEY" ]; then
            break;
        else
            echo -e "${RED}OpenRouter API Key cannot be blank!${NC}"
        fi
    done

    # Prompt for Discord Bot Token (Required for Gateway routing in this bundle)
    while true; do
        read -rp "Enter Discord Bot Token (Required): " DISCORD_TOKEN
        if [ -n "$DISCORD_TOKEN" ]; then
            break;
        else
            echo -e "${RED}Discord Bot Token cannot be blank!${NC}"
        fi
    done
    
    # Generate cryptographic secrets automatically if not supplied
    BETTER_AUTH_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)
    JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)
    INITIAL_PASSWORD=$(openssl rand -hex 12 2>/dev/null || head -c 12 /dev/urandom | xargs -0 | sha256sum | cut -c 1-12)
    DASHBOARD_PASSWORD=$(openssl rand -hex 12 2>/dev/null || head -c 12 /dev/urandom | xargs -0 | sha256sum | cut -c 1-12)
    DASHBOARD_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)

    cat <<ENVEOF > .env
# OpenIntent Shared Environment Variables
OPENROUTER_API_KEY=${OPENROUTER_KEY}
DISCORD_BOT_TOKEN=${DISCORD_TOKEN}
BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
JWT_SECRET=${JWT_SECRET}
INITIAL_PASSWORD=${INITIAL_PASSWORD}

# Dashboard Basic Auth & Session Secrets
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD}
DASHBOARD_SECRET=${DASHBOARD_SECRET}
# Internal Compose Network Endpoints
# 9ROUTER_API_KEY is generated at runtime by the bootstrap container
# using 9router's own POST /api/keys endpoint
HINDSIGHT_API_URL=http://hindsight-api:8888
9ROUTER_API_BASE=http://9router:20128/v1
9ROUTER_PORT=20128
HINDSIGHT_PORT=9177
ENVEOF
    
    echo -e "${GREEN}-> .env file created successfully!${NC}"
    echo -e "${YELLOW}Default Admin Password generated for 9router: ${INITIAL_PASSWORD}${NC}"
    echo -e "${YELLOW}Default Admin Username for Dashboard: admin${NC}"
    echo -e "${YELLOW}Default Admin Password for Dashboard: ${DASHBOARD_PASSWORD}${NC} (saved securely in .env)"
else
    echo -e "${GREEN}-> .env file already exists. Skipping prompts.${NC}"
fi

# 4. Bootstrap runtime profiles folders
echo -e "\nInitializing output directories..."
mkdir -p data/hermes
mkdir -p data/hermes/profiles/corporate-agent
mkdir -p data/hermes/profiles/public-agent

# Staging profile distributions templates
cp -rf profiles/default/* data/hermes/ 2>/dev/null || true
cp -rf profiles/corporate-agent/* data/hermes/profiles/corporate-agent/ 2>/dev/null || true
cp -rf profiles/public-agent/* data/hermes/profiles/public-agent/ 2>/dev/null || true

# Copy script endpoints
cp -f scripts/discord_setup.py data/hermes/discord_setup.py 2>/dev/null || true

# Bind env variables securely
cp -f .env data/hermes/.env
cp -f .env data/hermes/profiles/corporate-agent/.env
cp -f .env data/hermes/profiles/public-agent/.env

# Clean junk/orphaned profile YAML placeholders if left in config folder
rm -f config/*-profile.yaml 2>/dev/null || true

# Making script endpoints executable
chmod +x scripts/verify.sh
chmod +x scripts/discord_setup.py
chmod +x scripts/init_9router_db.py

echo -e "\n${GREEN}===============================================${NC}"
echo -e "${GREEN} OpenIntent Kit setup complete!               ${NC}"
echo -e "${GREEN} Disetup langsung di: data/hermes/profiles/    ${NC}"
echo -e "   1. Run: docker compose up -d                "
echo -e "      (This pulls and spins up all containers, including the bootstrap"
echo -e "       container that automatically sets up 9router credentials)"
echo -e "   2. Run: ./scripts/verify.sh                 "
echo -e "   3. Run: ./scripts/discord_setup.py          "
echo -e "${GREEN}===============================================${NC}"