# 🎯 Project Context: jm-monitor

## 1. 项目目标 (Core Goals)
构建一个工业级、高可用的微服务分布式监控系统（JM-Monitor）。
* **被动监控**：接收外部系统的心跳上报，维护状态机。
* **主动监控**：定时轮询探测内网微服务存活状态。
* **实时告警**：故障时平滑触发状态变更，向飞书/Lark 发射高亮互动卡片。

## 2. 五层分层架构 (Architecture Blueprint)
* 详见下文或 `docs/arch_5_layers.png`

## 3. 技术栈 (Tech Stack)
* **基础设施自动化**：Terraform (规划中)
* **物理云资产**：阿里云 ECS (Ubuntu 24.04 LTS)
* **运行环境/编排**：Docker / Docker Compose -> Kubernetes (演进中)
* **反向代理/网关**：Nginx
* **应用层**：Python 3.11 / Flask
* **流水线 (CI/CD)**：GitHub Actions (集成测试 + 阿里云 ACR 自动推流 + SSH 远程编排)

## 4. 当前进度 (Milestones)
* [x] Phase 1-3: 本地多容器网络通信与飞书告警状态机
* [x] Phase 4: 阿里云私有镜像仓库 (ACR) 对接与单机部署
* [x] Phase 5 (Current): GitHub Actions 自动化脱敏流水线全绿通车
* [ ] Phase 6 (Next): K8s 云原生重构

## 5. 当前阻碍与聚焦 (Current Issues)
1. 沉淀五层架构图，建立宏观分层思维。
2. 攻克 K8s 配置中心概念（ConfigMap & Secret）。
