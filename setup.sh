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
# =============================================================================
# OpenIntent Shared Core Environment Variables
# =============================================================================
OPENROUTER_API_KEY=${OPENROUTER_KEY}
DISCORD_BOT_TOKEN=${DISCORD_TOKEN}
BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
JWT_SECRET=${JWT_SECRET}
INITIAL_PASSWORD=${INITIAL_PASSWORD}

# Dashboard Basic Auth & Session Secrets
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD}
DASHBOARD_SECRET=${DASHBOARD_SECRET}

# =============================================================================
# Internal Compose Network Endpoints
# =============================================================================
HINDSIGHT_API_URL=http://hindsight-api:8888
9ROUTER_API_BASE=http://9router:20128/v1
9ROUTER_PORT=20128
HINDSIGHT_PORT=9177
CAMOFOX_URL=http://camoufox-browser:9377

# =============================================================================
# Exa & Firecrawl Search Settings (User can fill optional keys)
# =============================================================================
EXA_API_KEY=
FIRECRAWL_API_KEY=
9ROUTER_MCP_AUTH_TOKEN=
CONTEXT7_API_KEY=

# =============================================================================
# Hindsight Vector Engine Settings
# =============================================================================
HINDSIGHT_TIMEOUT=120
HINDSIGHT_IDLE_TIMEOUT=300
HINDSIGHT_API_WORKER_ENABLED=false
HINDSIGHT_API_WORKER_MAX_SLOTS=2
HINDSIGHT_API_WORKER_CONSOLIDATION_MAX_SLOTS=1
HINDSIGHT_API_WORKER_RETAIN_MAX_SLOTS=1
HINDSIGHT_API_WORKER_FILE_CONVERT_RETAIN_MAX_SLOTS=0
HINDSIGHT_API_WORKER_REFRESH_MENTAL_MODEL_MAX_SLOTS=0
HINDSIGHT_API_WORKER_POLL_INTERVAL_MS=2000
HINDSIGHT_API_LLM_MAX_CONCURRENT=2
HINDSIGHT_API_RETAIN_LLM_MAX_CONCURRENT=1
HINDSIGHT_API_REFLECT_LLM_MAX_CONCURRENT=1
HINDSIGHT_API_CONSOLIDATION_LLM_MAX_CONCURRENT=1
HINDSIGHT_API_CONSOLIDATION_MAX_MEMORIES_PER_ROUND=20
HINDSIGHT_API_CONSOLIDATION_LLM_BATCH_SIZE=2
HINDSIGHT_API_CONSOLIDATION_SOURCE_FACTS_MAX_TOKENS=2048
HINDSIGHT_API_CONSOLIDATION_SOURCE_FACTS_MAX_TOKENS_PER_OBSERVATION=128
HINDSIGHT_API_DB_POOL_MIN_SIZE=1
HINDSIGHT_API_DB_POOL_MAX_SIZE=10
HINDSIGHT_API_RETAIN_MAX_CONCURRENT=1
HINDSIGHT_API_RETAIN_CHUNK_BATCH_SIZE=20
HINDSIGHT_API_RECALL_MAX_CONCURRENT=2
HINDSIGHT_API_RERANKER_LOCAL_MAX_CONCURRENT=1

# =============================================================================
# Discord Interaction Boundaries & Controls
# =============================================================================
DISCORD_ALLOWED_USERS=
DISCORD_ALLOWED_CHANNELS=*
DISCORD_FREE_RESPONSE_CHANNELS=
DISCORD_IGNORED_CHANNELS=
DISCORD_THREAD_REQUIRE_MENTION=true
DISCORD_NO_THREAD_CHANNELS=*
DISCORD_REQUIRE_MENTION=true
DISCORD_AUTO_THREAD=false
DISCORD_IGNORE_NO_MENTION=true
DISCORD_ALLOW_BOTS=mentions
DISCORD_ALLOW_MENTION_REPLIED_USER=false
DISCORD_REPEAT_MENTIONS_ON_SPLIT=false
HERMES_DISCORD_BOT_TEXT_BATCH_DELAY_SECONDS=2.5
DISCORD_HOME_CHANNEL=
DISCORD_HOME_CHANNEL_THREAD_ID=

# =============================================================================
# OpenAI Compatible Image Settings
# =============================================================================
OPENAI_COMPATIBLE_IMAGE_BASE_URL=http://9router:20128/v1
OPENAI_COMPATIBLE_IMAGE_MODEL=cx/gpt-5.5

# =============================================================================
# Secrets Manager, Linear, Github, Telegram, Email, and WhatsApp Integrations
# =============================================================================
DEFAULT_BWS_ACCESS_TOKEN=
CORPORATE_BWS_ACCESS_TOKEN=
PUBLIC_BWS_ACCESS_TOKEN=
LINEAR_MCP_ACCESS_TOKEN=
GITHUB_TOKEN=
LINEAR_MCP_AUTH=
NOTION_MCP_AUTH=
GROQ_API_KEY=
OBSIDIAN_VAULT_PATH=
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USERS=
TELEGRAM_HOME_CHANNEL=
NTFY_TOPIC=
NTFY_TOKEN=
EMAIL_ADDRESS=
EMAIL_PASSWORD=
EMAIL_HOME_ADDRESS=
EMAIL_HOME_ADDRESS_NAME=
EMAIL_POLL_INTERVAL=90
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_ALLOWED_USERS=
WHATSAPP_MODE=self-chat
WHATSAPP_ENABLED=true
WHATSAPP_ALLOWED_USERS=
API_SERVER_ENABLED=true
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
API_SERVER_KEY=
SUDO_PASSWORD=
TERMINAL_ENV=docker
TINKER_API_KEY=
WANDB_API_KEY=

# Thread controls
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
TOKENIZERS_PARALLELISM=false
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