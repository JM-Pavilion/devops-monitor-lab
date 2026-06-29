# JM-Monitor (Cloud-Native Observability Lab)

[![CI — Unit Tests](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml/badge.svg)](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml)
[![Master Pipeline](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/master-pipeline.yml/badge.svg)](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/master-pipeline.yml)

A production-grade cloud monitoring system demonstrating end-to-end DevOps practices: infrastructure-as-code, containerised deployment, automated CI/CD, and real-time observability with Prometheus & Grafana.

---

## 📸 Visual Showcase (核心战果展示)

*(💡 注：请将 docs/screenshots 目录下的截图路径替换到下方)*

* **Grafana 生产级大盘 & QPS 流量监控**
  ![Grafana Dashboard](docs/screenshots/grafana-dashboard.png)
  ![Grafana Dashboard](docs/screenshots/total.png)
* **JM RADAR 实时微服务探针面板**
  ![JM Radar](docs/screenshots/jm-radar.png)
  ![JM Radar](docs/screenshots/jm-metrics.png)
* **Grafana 动态告警与飞书 Webhook 自动化闭环**
  ![Alerting](docs/screenshots/feishu-alert.png)
* **Prometheus 原生指标抓取与时序分析**
  ![Prometheus](docs/screenshots/prometheus-metrics.png)
  ![Prometheus](docs/screenshots/status.png)

---

## 🏗️ Architecture

```text
GitHub Push → GitHub Actions (CI/CD)
                 ├─ Unit Tests (pytest)
                 ├─ docker build → Alibaba Cloud ACR
                 ├─ terraform plan (IaC preview)
                 └─ SSH deploy → Alibaba Cloud ECS
                                   ├─ Nginx (80/443)
                                   └─ Docker Compose Network
                                         ├─ jm-monitor (Flask, 10000) ── Active probes → Targets
                                         ├─ order-service (Mock, 80)
                                         ├─ prometheus (9090) ── Scrapes → /metrics
                                         └─ grafana (3000) ── Reads → Prometheus ── Alerts → Feishu

See docs/architecture.md for the full breakdown.

🛠️ Tech Stack
Layer	Technology
Cloud Provider	Alibaba Cloud (ECS, VPC, ACR, CMS)
IaC	Terraform (Alicloud provider)
CI/CD Pipeline	GitHub Actions (4-stage automated pipeline)
Containerization	Docker · Docker Compose
Backend & Probes	Python 3.11 · Flask · requests
Observability	Prometheus (Metrics) · Grafana (Dashboards & Alerting)
Alert Routing	Feishu Interactive Card Webhook
📂 Project Structure
Plaintext
jm-monitor/
├── backend/                  # Application layer
│   ├── monitor/
│   │   ├── app.py            # Flask app + Prometheus WSGI middleware
│   │   └── config.json       # Hot-reloadable target config
│   ├── Dockerfile            # Multi-stage production image
│   └── requirements.txt
├── monitor/                  # Container orchestration & Observability
│   ├── docker-compose.yml    # Production stack (Flask + Prom + Grafana)
│   ├── prometheus.yml        # Prometheus scrape configurations
│   └── deploy.sh             # One-shot deploy helper
├── k8s/                      # Cloud infrastructure
│   ├── terraform/            # Alibaba Cloud IaC (ECS, VPC)
│   └── manifests/            # K8s Deployment YAMLs
├── gitops/                   # CI/CD pipeline definitions
│   └── .github/workflows/
└── docs/                     # Architecture & Screenshots
🚀 Quick Start
Prerequisites
Docker & Docker Compose
Copy .env.example → .env and configure your FEISHU_WEBHOOK_URL
Run locally (Production Stack)
Bash
cd monitor/
docker compose up -d --build
Access Points:
JM Radar UI: http://localhost:10000
Raw Metrics: http://localhost:10000/metrics
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (default: admin/admin)
🧠 Key Engineering Decisions
1. Unified Observability Triangle
Integrated standard prometheus_client into the Flask app to expose a /metrics endpoint. Prometheus scrapes this data periodically, and Grafana visualizes it while managing threshold-based alert routing to Feishu.
2. Multi-stage Dockerfile
Dependencies are compiled in a builder stage; only the ~/.local packages and application source are copied into the final image — keeping the production image extremely lean.
3. State-Machine Alerting & Hot-Reload
The Python engine tracks the previous state of each target, firing Feishu alerts only on state transitions to prevent alert storms. Targets can be updated dynamically via config.json without restarting containers.
🗺️ Roadmap
[x] Phase 1–3: Multi-container Docker network + Feishu state-machine alerting
[x] Phase 4: Alibaba Cloud ACR private registry + ECS single-node deploy
[x] Phase 5: GitHub Actions 4-stage CI/CD pipeline
[x] Phase 7: Prometheus + Grafana observability layer (Completed)
[ ] Phase 6: Kubernetes cloud-native refactor (manifests in k8s/)
[ ] Phase 8: ArgoCD GitOps continuous delivery
License
MIT © 2026 JM DevOps Lab