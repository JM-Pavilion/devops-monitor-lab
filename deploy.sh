#!/bin/bash

# 定义变量，方便以后修改
IMAGE_NAME="jminng/jm-monitor:latest"
CONTAINER_NAME="jm-cloud-sim"

echo "🚀 Starting Deployment..."

# 1. 如果旧容器在运行，先把它杀掉 (清理现场)
docker rm -f $CONTAINER_NAME 2>/dev/null

# 2. 拉取最新镜像
docker pull $IMAGE_NAME

# 3. 启动新容器
docker run -d --name $CONTAINER_NAME -p 8080:10000 $IMAGE_NAME

echo "✅ Deployment successful! Service is running on http://localhost:8080"
