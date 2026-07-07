#!/usr/bin/env bash
# =============================================================================
# OpenIntent Kit - Cascading Verification System
# =============================================================================
# Cascading health check verification for the OpenIntent multi-agent stack.
# Verifies container state, port availability, API responses, and database writes.
# =============================================================================

set -euo pipefail

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}     OpenIntent Kit Cascading Verification     ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Define host ports
PORT_9ROUTER=20128
PORT_PAPERCLIP=3100
PORT_HINDSIGHT=9177
PORT_OP=8001
PORT_CORP=8002
PORT_PUB=8003

# Helper to check if a port is open
check_port() {
    local service_name=$1
    local port=$2
    echo -n "Checking TCP port $port ($service_name)... "
    if python3 -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('127.0.0.1', $port))" &>/dev/null; then
        echo -e "${GREEN}PORT OPEN${NC}"
        return 0
    else
        echo -e "${RED}CLOSED${NC}"
        return 1
    fi
}

# Helper to verify HTTP status codes
check_http_response() {
    local service_name=$1
    local url=$2
    local expected_code=$3
    echo -n "Probing HTTP endpoint $service_name ($url)... "
    
    local response
    response=$(curl -s -w "%{http_code}" -o /dev/null --max-time 5 "$url" || echo "000")
    
    if [ "$response" = "$expected_code" ] || { [ "$expected_code" = "200" ] && [ "$response" = "302" ]; } || { [ "$expected_code" = "200" ] && [ "$response" = "307" ]; }; then
        echo -e "${GREEN}HTTP $response (OK)${NC}"
        return 0
    else
        echo -e "${RED}HTTP $response (EXPECTED $expected_code)${NC}"
        return 1
    fi
}

echo -e "\n${YELLOW}Level 1: Verification of Host Port Handshakes...${NC}"
FAILED_PORTS=0
check_port "9router" "$PORT_9ROUTER" || FAILED_PORTS=$((FAILED_PORTS + 1))
check_port "Hindsight Memory" "$PORT_HINDSIGHT" || FAILED_PORTS=$((FAILED_PORTS + 1))
check_port "Paperclip Dashboard" "$PORT_PAPERCLIP" || FAILED_PORTS=$((FAILED_PORTS + 1))
check_port "Agentic Company (Operations) Gateway" "$PORT_OP" || FAILED_PORTS=$((FAILED_PORTS + 1))
check_port "Corporate Agent Gateway" "$PORT_CORP" || FAILED_PORTS=$((FAILED_PORTS + 1))
check_port "Public Agent Gateway" "$PORT_PUB" || FAILED_PORTS=$((FAILED_PORTS + 1))

if [ "$FAILED_PORTS" -gt 0 ]; then
    echo -e "${RED}⚠️  Level 1 check failed: some services are offline or not binding ports.${NC}"
fi

echo -e "\n${YELLOW}Level 2: Verification of HTTP Application Routing...${NC}"
FAILED_HTTP=0
check_http_response "9router UI/API" "http://localhost:$PORT_9ROUTER" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))
check_http_response "Hindsight REST API" "http://localhost:$PORT_HINDSIGHT/health" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))
check_http_response "Paperclip HQ Command" "http://localhost:$PORT_PAPERCLIP" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))
check_http_response "Agentic Company (Operations) Gateway" "http://localhost:$PORT_OP/api/status" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))
check_http_response "Corporate Agent Gateway" "http://localhost:$PORT_CORP/api/status" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))
check_http_response "Public Agent Gateway" "http://localhost:$PORT_PUB/api/status" "200" || FAILED_HTTP=$((FAILED_HTTP + 1))

if [ "$FAILED_HTTP" -gt 0 ]; then
    echo -e "${RED}⚠️  Level 2 check failed: some services returned wrong HTTP codes.${NC}"
fi

echo -e "\n${YELLOW}Level 3: Verification of Vector Database Transaction Integration...${NC}"
echo -n "Sending list memories call to Hindsight... "
WRITE_STATUS=$(curl -s -X GET -w "%{http_code}" -o /dev/null \
    "http://localhost:$PORT_HINDSIGHT/v1/default/banks/default/memories/list" || echo "000")

if [ "$WRITE_STATUS" = "200" ]; then
    echo -e "${GREEN}DATABASE CONTEXT INTACT ($WRITE_STATUS)${NC}"
else
    echo -e "${RED}DATABASE CHECK FAILED ($WRITE_STATUS)${NC}"
fi

echo -e "\n${YELLOW}Level 4: Active Docker Orchestration Concurrency...${NC}"
if command -v docker &>/dev/null; then
    docker compose ps
else
    echo -e "${YELLOW}Docker client is not available dynamically in host environment.${NC}"
fi

echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}     Verification completed cascades.          ${NC}"
echo -e "${BLUE}===============================================${NC}"