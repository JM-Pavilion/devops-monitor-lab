#!/usr/bin/env bash
# ============================================================
# deploy.sh — local / ECS one-shot deploy helper
# Run from: jm-monitor/monitor/
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}🚀 [1/4] Stopping existing stack...${NC}"
docker compose down --remove-orphans

echo -e "${GREEN}📦 [2/4] Pulling latest images...${NC}"
docker compose pull

echo -e "${GREEN}🏗️  [3/4] Building & launching the stack...${NC}"
docker compose up -d --build

echo -e "${GREEN}🔍 [4/4] Verifying container health...${NC}"
sleep 5
docker compose ps

echo -e "${GREEN}✅ Stack is up. Tail logs: docker compose logs -f jm-monitor${NC}"
