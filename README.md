# JM-Monitor

[![CI — Unit Tests](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml/badge.svg)](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml)
[![Master Pipeline](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/master-pipeline.yml/badge.svg)](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/master-pipeline.yml)

A production-grade cloud monitoring system demonstrating end-to-end DevOps practices: infrastructure-as-code, containerised deployment, automated CI/CD, and real-time alerting.

---

## Architecture

```
GitHub Push → GitHub Actions (CI/CD)
                 ├─ Unit Tests (pytest)
                 ├─ docker build → Alibaba Cloud ACR
                 ├─ terraform plan (IaC preview)
                 └─ SSH deploy → Alibaba Cloud ECS
                                   ├─ Nginx (80/443)
                                   └─ jm-monitor container (Flask, port 10000)
                                         ├─ Active probes → External services
                                         └─ Feishu Webhook alerts
```

See [`docs/architecture.md`](docs/architecture.md) for the full five-layer breakdown.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | Alibaba Cloud (ECS, VPC, ACR, CMS) |
| IaC | Terraform (Alicloud provider) |
| CI/CD | GitHub Actions (4-stage pipeline) |
| Containers | Docker · Docker Compose → Kubernetes (Phase 6) |
| Reverse Proxy | Nginx (TLS termination) |
| Backend | Python 3.11 · Flask |
| Alerting | Feishu Interactive Card Webhook |

---

## Project Structure

```
jm-monitor/
├── backend/                  # Application layer
│   ├── monitor/
│   │   ├── app.py            # Flask app + monitoring engine
│   │   └── config.json       # Hot-reloadable target config
│   ├── tests/
│   │   └── test_app.py       # pytest unit tests
│   ├── Dockerfile            # Multi-stage production image
│   └── requirements.txt
│
├── monitor/                  # Container orchestration
│   ├── docker-compose.yml    # Production stack
│   ├── docker-compose.dev.yml# Dev override (hot-reload + LocalStack)
│   └── deploy.sh             # One-shot deploy helper
│
├── k8s/                      # Cloud infrastructure
│   ├── terraform/            # Alibaba Cloud IaC (ECS, VPC, CMS)
│   │   ├── main.tf
│   │   ├── backend.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars.example
│   ├── deployment.yaml       # K8s Deployment (Phase 6)
│   ├── service.yaml          # K8s Service
│   ├── configmap.yaml        # K8s ConfigMap
│   └── namespace.yaml
│
├── gitops/                   # CI/CD pipeline definitions
│   └── .github/workflows/
│       ├── ci-test.yml       # PR/push: run pytest
│       ├── master-pipeline.yml # Full 4-stage pipeline
│       └── deploy.yml        # Standalone ACR build & ECS deploy
│
├── nginx/
│   └── jm-monitor.conf       # Reverse proxy config
│
├── docs/
│   ├── architecture.md       # System design & diagrams
│   └── data_flow_v1.md       # Data flow walkthrough
│
├── .env.example              # Environment variable template
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Copy `.env.example` → `.env` and fill in `FEISHU_WEBHOOK_URL`

### Run locally (production mode)

```bash
cd monitor/
docker compose up -d
# Dashboard → http://localhost:10000
```

### Run in development (hot-reload)

```bash
cd monitor/
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Code changes in `backend/monitor/app.py` apply instantly without rebuilding.

### Run tests

```bash
cd backend/
pip install -r requirements.txt pytest
pytest tests/ -v
```

---

## Key Engineering Decisions

### Multi-stage Dockerfile
Dependencies are compiled in a `builder` stage; only the `~/.local` packages and application source are copied into the final image — keeping the production image lean.

### State-machine alerting
The monitoring engine tracks the previous state of each target. A Feishu alert fires **only on state transitions** (Normal → Error, Error → Normal), eliminating alert storms during sustained outages.

### Hot-reloadable config
`config.json` is re-read on every polling cycle. Adding or removing monitoring targets requires no container restart.

### Named log volume (production)
Production Compose uses a named Docker volume (`jm_monitor_logs`) instead of a bind-mount, so logs survive container replacements without depending on host directory paths.

### Secrets management
All credentials (ACR password, ECS password, Feishu webhook) are injected at runtime via GitHub Secrets or environment variables. No secrets appear in source code or image layers.

---

## CI/CD Pipeline Stages

| Stage | Trigger | Action |
|---|---|---|
| `ci-test.yml` | Every push / PR | `pytest tests/` — blocks merge on failure |
| `master-pipeline.yml` Stage 1 | push to `main` | Run tests again |
| `master-pipeline.yml` Stage 2 | After tests pass | `docker build` → push `:sha` + `:latest` to ACR |
| `master-pipeline.yml` Stage 3 | After image push | `terraform plan` (read-only IaC preview) |
| `master-pipeline.yml` Stage 4 | After plan passes | SCP compose file → SSH `docker compose up -d` |

---

## Roadmap

- [x] Phase 1–3: Multi-container Docker network + Feishu state-machine alerting
- [x] Phase 4: Alibaba Cloud ACR private registry + ECS single-node deploy
- [x] Phase 5: GitHub Actions 4-stage CI/CD pipeline (full automation)
- [ ] Phase 6: Kubernetes cloud-native refactor (manifests in `k8s/`)
- [ ] Phase 7: Prometheus + Grafana observability layer
- [ ] Phase 8: ArgoCD GitOps continuous delivery

---

## License

MIT © 2026 JM DevOps Lab


