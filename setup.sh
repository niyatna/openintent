#!/usr/bin/env bash
# =============================================================================
# OpenIntent Kit - Interactive Provisioner
# =============================================================================
# Idempotent bootstrap installer for the OpenIntent multi-agent stack.
# Checks dependencies, provisions credentials, and sets up configurations.
# =============================================================================

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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
# Load existing environment configuration variables if .env exists
if [ -f .env ]; then
    echo -e "${BLUE}-> Existing .env configuration detected. Loading current values...${NC}"
    while IFS= read -r line || [ -n "$line" ]; do
        if [[ "$line" =~ ^[A-Za-z0-9_]+= ]]; then
            key=$(echo "$line" | cut -d= -f1)
            val=$(echo "$line" | cut -d= -f2-)
            # Strip outer single/double quotes
            val="${val#\"}"
            val="${val%\"}"
            val="${val#\'}"
            val="${val%\'}"
            eval "EXISTING_${key}=\"\$val\""
        fi
    done < .env
fi

echo -e "\n${YELLOW}Provisioning environment configuration credentials (.env)...${NC}"

prompt_env_var() {
    local var_name=$1
    local prompt_label=$2
    local is_required=$3
    
    local lookup="EXISTING_${var_name}"
    local existing_val="${!lookup:-}"
    local result_val=""
    local input_val=""
    
    while true; do
        if [ -n "$existing_val" ]; then
            local masked=""
            if [ ${#existing_val} -gt 8 ]; then
                masked="${existing_val:0:4}...${existing_val: -4}"
            else
                masked="******"
            fi
            read -rp "Enter $prompt_label (Current: $masked, ENTER to keep): " input_val || input_val=""
            if [ -z "$input_val" ]; then
                result_val="$existing_val"
                break
            else
                result_val="$input_val"
                break
            fi
        else
            local req_suffix=""
            if [ "$is_required" = "true" ]; then
                req_suffix=" (Required)"
            else
                req_suffix=" (Optional - Press ENTER to skip)"
            fi
            read -rp "Enter $prompt_label$req_suffix: " input_val || input_val=""
            if [ -n "$input_val" ]; then
                result_val="$input_val"
                break
            elif [ "$is_required" = "false" ]; then
                result_val=""
                break
            else
                if [ ! -t 0 ]; then
                    result_val="dummy-test-key-fallback"
                    break
                fi
                echo -e "${RED}$prompt_label is required and cannot be blank!${NC}"
            fi
        fi
    done
    
    eval "$var_name=\"\$result_val\""
}

# Prompting standard orchestration variables
prompt_env_var "OPENROUTER_API_KEY" "OpenRouter API Key" "true"

# Prompt to select which agent lanes to activate (ENTER/Default is Yes)
SETUP_OPERATIONS="true"
SETUP_CORPORATE="true"
SETUP_PUBLIC="true"

if [ -t 0 ]; then
    echo -e "\n${YELLOW}Which Agent Lanes would you like to set up and enable?${NC}"
    read -rp "1. Enable Operations/Default Agent (y/n) [Default: y]: " ans_op
    if [ "${ans_op,,}" = "n" ] || [ "${ans_op,,}" = "no" ]; then SETUP_OPERATIONS="false"; fi
    
    read -rp "2. Enable Corporate Agent (y/n) [Default: y]: " ans_corp
    if [ "${ans_corp,,}" = "n" ] || [ "${ans_corp,,}" = "no" ]; then SETUP_CORPORATE="false"; fi
    
    read -rp "3. Enable Public Agent (y/n) [Default: y]: " ans_pub
    if [ "${ans_pub,,}" = "n" ] || [ "${ans_pub,,}" = "no" ]; then SETUP_PUBLIC="false"; fi
fi

if [ "$SETUP_OPERATIONS" = "true" ]; then
    echo -e "\n${BLUE}--- Operations/Default Agent Configuration ---${NC}"
    prompt_env_var "DISCORD_BOT_TOKEN_OPERATIONS" "Discord Bot Token for Operations Agent" "false"
    prompt_env_var "TELEGRAM_BOT_TOKEN_OPERATIONS" "Telegram Bot Token for Operations Agent" "false"
    prompt_env_var "EMAIL_ADDRESS_OPERATIONS" "Email Address for Operations Agent" "false"
    prompt_env_var "EMAIL_PASSWORD_OPERATIONS" "Email Password for Operations Agent" "false"
    prompt_env_var "SLACK_BOT_TOKEN_OPERATIONS" "Slack Bot Token for Operations Agent" "false"
    prompt_env_var "SLACK_APP_TOKEN_OPERATIONS" "Slack App Token for Operations Agent" "false"
    prompt_env_var "DEFAULT_BWS_ACCESS_TOKEN" "Bitwarden Access Token for Operations Agent" "false"
    prompt_env_var "GITHUB_TOKEN_OPERATIONS" "GitHub Token for Operations Agent" "false"
    prompt_env_var "LINEAR_MCP_ACCESS_TOKEN_OPERATIONS" "Linear Token for Operations Agent" "false"
else
    DISCORD_BOT_TOKEN_OPERATIONS=""
    TELEGRAM_BOT_TOKEN_OPERATIONS=""
    EMAIL_ADDRESS_OPERATIONS=""
    EMAIL_PASSWORD_OPERATIONS=""
    SLACK_BOT_TOKEN_OPERATIONS=""
    SLACK_APP_TOKEN_OPERATIONS=""
    DEFAULT_BWS_ACCESS_TOKEN=""
    GITHUB_TOKEN_OPERATIONS=""
    LINEAR_MCP_ACCESS_TOKEN_OPERATIONS=""
fi

if [ "$SETUP_CORPORATE" = "true" ]; then
    echo -e "\n${BLUE}--- Corporate Agent Configuration ---${NC}"
    prompt_env_var "DISCORD_BOT_TOKEN_CORPORATE" "Discord Bot Token for Corporate Agent" "false"
    prompt_env_var "TELEGRAM_BOT_TOKEN_CORPORATE" "Telegram Bot Token for Corporate Agent" "false"
    prompt_env_var "EMAIL_ADDRESS_CORPORATE" "Email Address for Corporate Agent" "false"
    prompt_env_var "EMAIL_PASSWORD_CORPORATE" "Email Password for Corporate Agent" "false"
    prompt_env_var "SLACK_BOT_TOKEN_CORPORATE" "Slack Bot Token for Corporate Agent" "false"
    prompt_env_var "SLACK_APP_TOKEN_CORPORATE" "Slack App Token for Corporate Agent" "false"
    prompt_env_var "CORPORATE_BWS_ACCESS_TOKEN" "Bitwarden Access Token for Corporate Agent" "false"
    prompt_env_var "GITHUB_TOKEN_CORPORATE" "GitHub Token for Corporate Agent" "false"
    prompt_env_var "LINEAR_MCP_ACCESS_TOKEN_CORPORATE" "Linear Token for Corporate Agent" "false"
else
    DISCORD_BOT_TOKEN_CORPORATE=""
    TELEGRAM_BOT_TOKEN_CORPORATE=""
    EMAIL_ADDRESS_CORPORATE=""
    EMAIL_PASSWORD_CORPORATE=""
    SLACK_BOT_TOKEN_CORPORATE=""
    SLACK_APP_TOKEN_CORPORATE=""
    CORPORATE_BWS_ACCESS_TOKEN=""
    GITHUB_TOKEN_CORPORATE=""
    LINEAR_MCP_ACCESS_TOKEN_CORPORATE=""
fi

if [ "$SETUP_PUBLIC" = "true" ]; then
    echo -e "\n${BLUE}--- Public Agent Configuration ---${NC}"
    prompt_env_var "DISCORD_BOT_TOKEN_PUBLIC" "Discord Bot Token for Public Agent" "false"
    prompt_env_var "TELEGRAM_BOT_TOKEN_PUBLIC" "Telegram Bot Token for Public Agent" "false"
    prompt_env_var "EMAIL_ADDRESS_PUBLIC" "Email Address for Public Agent" "false"
    prompt_env_var "EMAIL_PASSWORD_PUBLIC" "Email Password for Public Agent" "false"
    prompt_env_var "SLACK_BOT_TOKEN_PUBLIC" "Slack Bot Token for Public Agent" "false"
    prompt_env_var "SLACK_APP_TOKEN_PUBLIC" "Slack App Token for Public Agent" "false"
    prompt_env_var "PUBLIC_BWS_ACCESS_TOKEN" "Bitwarden Access Token for Public Agent" "false"
    prompt_env_var "GITHUB_TOKEN_PUBLIC" "GitHub Token for Public Agent" "false"
    prompt_env_var "LINEAR_MCP_ACCESS_TOKEN_PUBLIC" "Linear Token for Public Agent" "false"
else
    DISCORD_BOT_TOKEN_PUBLIC=""
    TELEGRAM_BOT_TOKEN_PUBLIC=""
    EMAIL_ADDRESS_PUBLIC=""
    EMAIL_PASSWORD_PUBLIC=""
    SLACK_BOT_TOKEN_PUBLIC=""
    SLACK_APP_TOKEN_PUBLIC=""
    PUBLIC_BWS_ACCESS_TOKEN=""
    GITHUB_TOKEN_PUBLIC=""
    LINEAR_MCP_ACCESS_TOKEN_PUBLIC=""
fi
# Global Integration Keys
prompt_env_var "CONTEXT7_API_KEY" "Context7 API Key" "false"
prompt_env_var "EXA_API_KEY" "Exa API Key" "false"
prompt_env_var "FIRECRAWL_API_KEY" "Firecrawl API Key" "false"
prompt_env_var "GROQ_API_KEY" "Groq API Key" "false"

# Build fallback variables for orchestration
DISCORD_TOKEN="${DISCORD_BOT_TOKEN_OPERATIONS:-${DISCORD_BOT_TOKEN_CORPORATE:-$DISCORD_BOT_TOKEN_PUBLIC}}"
TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN_OPERATIONS:-${TELEGRAM_BOT_TOKEN_CORPORATE:-$TELEGRAM_BOT_TOKEN_PUBLIC}}"
EMAIL_ADDRESS="${EMAIL_ADDRESS_OPERATIONS:-${EMAIL_ADDRESS_CORPORATE:-$EMAIL_ADDRESS_PUBLIC}}"
EMAIL_PASSWORD="${EMAIL_PASSWORD_OPERATIONS:-${EMAIL_PASSWORD_CORPORATE:-$EMAIL_PASSWORD_PUBLIC}}"
SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN_OPERATIONS:-${SLACK_BOT_TOKEN_CORPORATE:-$SLACK_BOT_TOKEN_PUBLIC}}"
SLACK_APP_TOKEN="${SLACK_APP_TOKEN_OPERATIONS:-${SLACK_APP_TOKEN_CORPORATE:-$SLACK_APP_TOKEN_PUBLIC}}"
GITHUB_TOKEN="${GITHUB_TOKEN_OPERATIONS:-${GITHUB_TOKEN_CORPORATE:-$GITHUB_TOKEN_PUBLIC}}"
LINEAR_MCP_ACCESS_TOKEN="${LINEAR_MCP_ACCESS_TOKEN_OPERATIONS:-${LINEAR_MCP_ACCESS_TOKEN_CORPORATE:-$LINEAR_MCP_ACCESS_TOKEN_PUBLIC}}"
OPENROUTER_KEY="${OPENROUTER_API_KEY}"

# Resolve or generate 9router API key
EXISTING_9ROUTER_KEY="${EXISTING_9ROUTER_API_KEY:-}"
if [ -z "$EXISTING_9ROUTER_KEY" ] && [ -f data/9router/.niyatna-9router-key ]; then
    EXISTING_9ROUTER_KEY=$(cat data/9router/.niyatna-9router-key 2>/dev/null || true)
fi

if [ -n "$EXISTING_9ROUTER_KEY" ]; then
    ROUTER_API_KEY="$EXISTING_9ROUTER_KEY"
else
    AGENT_KEY=$(openssl rand -hex 12 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(12))")
    ROUTER_API_KEY="sk-niyatna-agent-${AGENT_KEY}"
fi

# Write key configuration files for 9router & Hindsight API dependencies
mkdir -p data/9router
echo "$ROUTER_API_KEY" > data/9router/.niyatna-9router-key
chmod 644 data/9router/.niyatna-9router-key
cat << KEYEOF > data/9router/.agent.env
9ROUTER_API_KEY=${ROUTER_API_KEY}
HINDSIGHT_API_KEY=${ROUTER_API_KEY}
HINDSIGHT_API_LLM_API_KEY=${ROUTER_API_KEY}
HINDSIGHT_LLM_API_KEY=${ROUTER_API_KEY}
KEYEOF
chmod 644 data/9router/.agent.env

BETTER_AUTH_SECRET=${EXISTING_BETTER_AUTH_SECRET:-$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)}
JWT_SECRET=${EXISTING_JWT_SECRET:-$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)}
INITIAL_PASSWORD=${EXISTING_INITIAL_PASSWORD:-$(openssl rand -hex 12 2>/dev/null || head -c 12 /dev/urandom | xargs -0 | sha256sum | cut -c 1-12)}
DASHBOARD_PASSWORD=${EXISTING_DASHBOARD_PASSWORD:-$(openssl rand -hex 12 2>/dev/null || head -c 12 /dev/urandom | xargs -0 | sha256sum | cut -c 1-12)}
DASHBOARD_SECRET=${EXISTING_DASHBOARD_SECRET:-$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xargs -0 | sha256sum | cut -d' ' -f1)}
HOST_UID=${EXISTING_HERMES_UID:-$(id -u "${SUDO_USER:-$USER}")}
HOST_GID=${EXISTING_HERMES_GID:-$(id -g "${SUDO_USER:-$USER}")}
    cat <<ENVEOF > .env
# =============================================================================
# Claude Code (CLI) Redirect Custom Variables
# =============================================================================
ANTHROPIC_BASE_URL=http://localhost:20128/v1
ANTHROPIC_AUTH_TOKEN=niyatna-agent-token
ANTHROPIC_MODEL=oc/deepseek-v4-flash-free

# =============================================================================
# OpenIntent Shared Core Environment Variables
# =============================================================================
OPENROUTER_API_KEY=${OPENROUTER_KEY}
9ROUTER_API_KEY=${ROUTER_API_KEY}
DISCORD_BOT_TOKEN_OPERATIONS=${DISCORD_BOT_TOKEN_OPERATIONS:-}
DISCORD_BOT_TOKEN_CORPORATE=${DISCORD_BOT_TOKEN_CORPORATE:-}
DISCORD_BOT_TOKEN_PUBLIC=${DISCORD_BOT_TOKEN_PUBLIC:-}
DISCORD_BOT_TOKEN=${DISCORD_TOKEN:-}
BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
JWT_SECRET=${JWT_SECRET}
INITIAL_PASSWORD=${INITIAL_PASSWORD}

# Dashboard Basic Auth & Session Secrets
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD}
DASHBOARD_SECRET=${DASHBOARD_SECRET}
PAPERCLIP_PUBLIC_URL=http://localhost:3100
PAPERCLIP_ALLOWED_HOSTNAMES=localhost
HERMES_UID=${HOST_UID}
HERMES_GID=${HOST_GID}

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
EXA_API_KEY=${EXA_API_KEY:-}
FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY:-}
CONTEXT7_API_KEY=${CONTEXT7_API_KEY:-}

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
DEFAULT_BWS_ACCESS_TOKEN=${DEFAULT_BWS_ACCESS_TOKEN:-}
CORPORATE_BWS_ACCESS_TOKEN=${CORPORATE_BWS_ACCESS_TOKEN:-}
PUBLIC_BWS_ACCESS_TOKEN=${PUBLIC_BWS_ACCESS_TOKEN:-}

TELEGRAM_BOT_TOKEN_OPERATIONS=${TELEGRAM_BOT_TOKEN_OPERATIONS:-}
TELEGRAM_BOT_TOKEN_CORPORATE=${TELEGRAM_BOT_TOKEN_CORPORATE:-}
TELEGRAM_BOT_TOKEN_PUBLIC=${TELEGRAM_BOT_TOKEN_PUBLIC:-}

EMAIL_ADDRESS_OPERATIONS=${EMAIL_ADDRESS_OPERATIONS:-}
EMAIL_PASSWORD_OPERATIONS=${EMAIL_PASSWORD_OPERATIONS:-}
EMAIL_ADDRESS_CORPORATE=${EMAIL_ADDRESS_CORPORATE:-}
EMAIL_PASSWORD_CORPORATE=${EMAIL_PASSWORD_CORPORATE:-}
EMAIL_ADDRESS_PUBLIC=${EMAIL_ADDRESS_PUBLIC:-}
EMAIL_PASSWORD_PUBLIC=${EMAIL_PASSWORD_PUBLIC:-}

SLACK_BOT_TOKEN_OPERATIONS=${SLACK_BOT_TOKEN_OPERATIONS:-}
SLACK_APP_TOKEN_OPERATIONS=${SLACK_APP_TOKEN_OPERATIONS:-}
SLACK_BOT_TOKEN_CORPORATE=${SLACK_BOT_TOKEN_CORPORATE:-}
SLACK_APP_TOKEN_CORPORATE=${SLACK_APP_TOKEN_CORPORATE:-}
SLACK_BOT_TOKEN_PUBLIC=${SLACK_BOT_TOKEN_PUBLIC:-}
SLACK_APP_TOKEN_PUBLIC=${SLACK_APP_TOKEN_PUBLIC:-}

GITHUB_TOKEN_OPERATIONS=${GITHUB_TOKEN_OPERATIONS:-}
GITHUB_TOKEN_CORPORATE=${GITHUB_TOKEN_CORPORATE:-}
GITHUB_TOKEN_PUBLIC=${GITHUB_TOKEN_PUBLIC:-}

LINEAR_MCP_ACCESS_TOKEN_OPERATIONS=${LINEAR_MCP_ACCESS_TOKEN_OPERATIONS:-}
LINEAR_MCP_ACCESS_TOKEN_CORPORATE=${LINEAR_MCP_ACCESS_TOKEN_CORPORATE:-}
LINEAR_MCP_ACCESS_TOKEN_PUBLIC=${LINEAR_MCP_ACCESS_TOKEN_PUBLIC:-}

LINEAR_MCP_ACCESS_TOKEN=${LINEAR_MCP_ACCESS_TOKEN:-}
GITHUB_TOKEN=${GITHUB_TOKEN:-}
GITHUB_APP_ID=
GITHUB_APP_PRIVATE_KEY_PATH=
GITHUB_APP_INSTALLATION_ID=
LINEAR_MCP_AUTH=
NOTION_MCP_AUTH=
GROQ_API_KEY=${GROQ_API_KEY:-}
STT_GROQ_MODEL=whisper-large-v3-turbo
STT_OPENAI_MODEL=whisper-1
OBSIDIAN_VAULT_PATH=
TELEGRAM_BOT_TOKEN=${TELEGRAM_TOKEN:-}
TELEGRAM_ALLOWED_USERS=
TELEGRAM_HOME_CHANNEL=
TELEGRAM_HOME_CHANNEL_NAME=
TELEGRAM_WEBHOOK_URL=
TELEGRAM_WEBHOOK_PORT=8443
TELEGRAM_WEBHOOK_SECRET=
SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN:-}
SLACK_APP_TOKEN=${SLACK_APP_TOKEN:-}
SLACK_ALLOWED_USERS=
EMAIL_ADDRESS=${EMAIL_ADDRESS:-}
EMAIL_PASSWORD=${EMAIL_PASSWORD:-}
EMAIL_SMTP_PORT=587
EMAIL_IMAP_PORT=993
EMAIL_HOME_ADDRESS=
EMAIL_HOME_ADDRESS_NAME=
EMAIL_POLL_INTERVAL=90
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_ALLOWED_USERS=
WHATSAPP_MODE=self-chat
WHATSAPP_ENABLED=false
WHATSAPP_ALLOWED_USERS=
API_SERVER_ENABLED=true
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
API_SERVER_KEY=
SUDO_PASSWORD=
TERMINAL_ENV=docker
TERMINAL_TIMEOUT=60
TERMINAL_LIFETIME_SECONDS=300
HERMES_HUMAN_DELAY_MIN_MS=800
TERMINAL_SSH_HOST=
TERMINAL_SSH_USER=
TERMINAL_SSH_PORT=22
TERMINAL_SSH_KEY=~/.ssh/id_rsa
TINKER_API_KEY=
WANDB_API_KEY=

# Thread controls
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
TOKENIZERS_PARALLELISM=false
ENVEOF
    
    echo -e "${GREEN}-> .env file configured successfully!${NC}"
    echo -e "${YELLOW}Default Admin Password generated for 9router: ${INITIAL_PASSWORD}${NC}"
    echo -e "${YELLOW}Default Admin Username for Dashboard: admin${NC}"
    echo -e "${YELLOW}Default Admin Password for Dashboard: ${DASHBOARD_PASSWORD}${NC} (saved securely in .env)"


# 4. Bootstrap runtime profiles folders
echo -e "\nInitializing output directories..."
mkdir -p data/hermes
mkdir -p data/hermes/profiles/corporate-agent
mkdir -p data/hermes/profiles/public-agent
mkdir -p data/9router
mkdir -p data/hindsight
mkdir -p data/paperclip
mkdir -p data/camoufox
mkdir -p data/postgres

# Ensure writable permissions for non-root container users (UID 1000/70/etc.)
chmod -R 777 data
# PostgreSQL requires strict permissions (0700) on its data directory
chmod -R 700 data/hindsight
# Staging profile distributions templates
cp -rf profiles/default/* data/hermes/ 2>/dev/null || true
cp -rf profiles/corporate-agent/* data/hermes/profiles/corporate-agent/ 2>/dev/null || true
cp -rf profiles/public-agent/* data/hermes/profiles/public-agent/ 2>/dev/null || true

# Copy script endpoints
cp -f scripts/discord_setup.py data/hermes/discord_setup.py 2>/dev/null || true

# Bind env variables securely
map_profile_env() {
    local example_file=$1
    local env_file=$2
    local pfx=$3 # OPERATIONS, CORPORATE, PUBLIC

    if [ -f "$example_file" ]; then
        # 1. Start with a clean copy of the profile's EXAMPLE
        cp -f "$example_file" "$env_file"

        # 2. Fill standard keys matching from root .env
        while IFS= read -r line || [ -n "$line" ]; do
            if [[ "$line" =~ ^[A-Za-z0-9_]+= ]]; then
                local key=$(echo "$line" | cut -d= -f1)
                local val=$(echo "$line" | cut -d= -f2-)
                if grep -q "^${key}=" "$env_file" 2>/dev/null; then
                    sed -i "s|^${key}=.*|${key}=${val}|" "$env_file"
                fi
            fi
        done < .env

        # 3. Map profile-specific platform credentials to standard Hermes names
        # Map Discord
        local disc_tok=$(grep "^DISCORD_BOT_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        if [ "$pfx" = "OPERATIONS" ]; then
            disc_tok=${disc_tok:-$(grep "^DISCORD_BOT_TOKEN=" .env 2>/dev/null | cut -d'=' -f2- || true)}
        fi
        sed -i "s|^DISCORD_BOT_TOKEN=.*|DISCORD_BOT_TOKEN=${disc_tok}|" "$env_file"

        # Map Telegram
        local tg_tok=$(grep "^TELEGRAM_BOT_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        sed -i "s|^TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=${tg_tok}|" "$env_file"

        # Map Email
        local mail_addr=$(grep "^EMAIL_ADDRESS_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        local mail_pwd=$(grep "^EMAIL_PASSWORD_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        sed -i "s|^EMAIL_ADDRESS=.*|EMAIL_ADDRESS=${mail_addr}|" "$env_file"
        sed -i "s|^EMAIL_PASSWORD=.*|EMAIL_PASSWORD=${mail_pwd}|" "$env_file"

        # Map Slack
        local sl_bot=$(grep "^SLACK_BOT_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        local sl_app=$(grep "^SLACK_APP_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        sed -i "s|^SLACK_BOT_TOKEN=.*|SLACK_BOT_TOKEN=${sl_bot}|" "$env_file"
        sed -i "s|^SLACK_APP_TOKEN=.*|SLACK_APP_TOKEN=${sl_app}|" "$env_file"

        # Map Bitwarden Secrets Manager (BWS_ACCESS_TOKEN)
        local bws_var="DEFAULT_BWS_ACCESS_TOKEN"
        if [ "$pfx" = "CORPORATE" ]; then bws_var="CORPORATE_BWS_ACCESS_TOKEN"; fi
        if [ "$pfx" = "PUBLIC" ]; then bws_var="PUBLIC_BWS_ACCESS_TOKEN"; fi
        local bws_tok=$(grep "^${bws_var}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        
        if grep -q "^BWS_ACCESS_TOKEN=" "$env_file" 2>/dev/null; then
            sed -i "s|^BWS_ACCESS_TOKEN=.*|BWS_ACCESS_TOKEN=${bws_tok}|" "$env_file"
        elif grep -q "^${bws_var}=" "$env_file" 2>/dev/null; then
            sed -i "s|^${bws_var}=.*|${bws_var}=${bws_tok}|" "$env_file"
        else
            echo "BWS_ACCESS_TOKEN=${bws_tok}" >> "$env_file"
        fi

        # Map GitHub & Linear
        local gh_tok=$(grep "^GITHUB_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        local lin_tok=$(grep "^LINEAR_MCP_ACCESS_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
        sed -i "s|^GITHUB_TOKEN=.*|GITHUB_TOKEN=${gh_tok}|" "$env_file"
        sed -i "s|^LINEAR_MCP_ACCESS_TOKEN=.*|LINEAR_MCP_ACCESS_TOKEN=${lin_tok}|" "$env_file"
    fi
}

map_profile_env "profiles/default/.env.EXAMPLE" "data/hermes/.env" "OPERATIONS"
echo "TERMINAL_CWD=/opt/data/company-brain" >> data/hermes/.env

map_profile_env "profiles/corporate-agent/.env.EXAMPLE" "data/hermes/profiles/corporate-agent/.env" "CORPORATE"
echo "TERMINAL_CWD=/opt/data/profiles/corporate-agent/corporate-brain" >> data/hermes/profiles/corporate-agent/.env

map_profile_env "profiles/public-agent/.env.EXAMPLE" "data/hermes/profiles/public-agent/.env" "PUBLIC"
echo "TERMINAL_CWD=/opt/data/profiles/public-agent/public-brain" >> data/hermes/profiles/public-agent/.env

# Dynamically update platforms status in config.yaml per profile
update_platforms_status() {
    local config_file=$1
    local pfx=$2

    local discord_token=$(grep "^DISCORD_BOT_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
    if [ "$pfx" = "OPERATIONS" ]; then
        discord_token=${discord_token:-$(grep "^DISCORD_BOT_TOKEN=" .env 2>/dev/null | cut -d'=' -f2- || true)}
    fi
    local telegram_token=$(grep "^TELEGRAM_BOT_TOKEN_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)
    local email_addr=$(grep "^EMAIL_ADDRESS_${pfx}=" .env 2>/dev/null | cut -d'=' -f2- || true)

    if [ -f "$config_file" ]; then
        python3 -c "
import sys, yaml
path = sys.argv[1]
has_discord = bool(sys.argv[2])
has_telegram = bool(sys.argv[3])
has_email = bool(sys.argv[4])
try:
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    if isinstance(data, dict) and 'platforms' in data:
        if 'discord' in data['platforms']:
            data['platforms']['discord']['enabled'] = has_discord
        if 'telegram' in data['platforms']:
            data['platforms']['telegram']['enabled'] = has_telegram
        if 'email' in data['platforms']:
            data['platforms']['email']['enabled'] = has_email
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False)
except Exception:
    pass
" "$config_file" "${discord_token}" "${telegram_token}" "${email_addr}" 2>/dev/null || true
    fi
}

update_platforms_status "data/hermes/config.yaml" "OPERATIONS"
update_platforms_status "data/hermes/profiles/corporate-agent/config.yaml" "CORPORATE"
update_platforms_status "data/hermes/profiles/public-agent/config.yaml" "PUBLIC"

# Clean junk/orphaned profile YAML placeholders if left in config folder
rm -f config/*-profile.yaml 2>/dev/null || true

# Auto-inject Claude Code CLI redirection parameters to host shell configuration dynamically
SHELL_CONFIG=""
if [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "ANTHROPIC_BASE_URL" "$SHELL_CONFIG"; then
        echo -e "\n# Claude Code redirect configuration for OpenIntent" >> "$SHELL_CONFIG"
        echo 'export ANTHROPIC_BASE_URL="http://localhost:20128/v1"' >> "$SHELL_CONFIG"
        echo 'export ANTHROPIC_AUTH_TOKEN="niyatna-agent-token"' >> "$SHELL_CONFIG"
        echo 'export ANTHROPIC_MODEL="oc/deepseek-v4-flash-free"' >> "$SHELL_CONFIG"
        echo -e "${GREEN}-> Added Claude Code proxy redirects to $SHELL_CONFIG!${NC}"
    fi
fi
# Making script endpoints executable
chmod +x scripts/verify.sh
chmod +x scripts/discord_setup.py
chmod +x scripts/init_9router_db.py

echo -e "\n${GREEN}===============================================${NC}"
echo -e "${GREEN} OpenIntent Kit setup complete!               ${NC}"
echo -e "${GREEN} Disetup langsung di: data/hermes/profiles/    ${NC}"
echo -e "   1. Run: docker compose --profile agents up -d"
echo -e "      (This pulls and spins up all containers, including the bootstrap"
echo -e "       container that automatically sets up 9router credentials)"
echo -e "   2. Run: ./scripts/verify.sh                 "
echo -e "   3. Run: ./scripts/discord_setup.py          "
echo -e "${GREEN}===============================================${NC}"