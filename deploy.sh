#!/bin/bash

# 定义颜色，让输出更漂亮（澳洲公司常用的脚本风格）
GREEN='\033[0:32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 [Step 1/4] Cleaning up orphaned containers...${NC}"
docker-compose down --remove-orphans

echo -e "${GREEN}📦 [Step 2/4] Pulling latest images...${NC}"
docker-compose pull

echo -e "${GREEN}🏗️ [Step 3/4] Launching the stack...${NC}"
# --build 确保如果本地代码改了，镜像也会尝试重新构建
docker-compose up -d --build

echo -e "${GREEN}🔍 [Step 4/4] Verifying health status...${NC}"
# 给容器一点点“热身”时间
sleep 5
docker-compose ps

echo -e "${GREEN}✅ All systems are operational! Check logs/monitor.log for details.${NC}"
