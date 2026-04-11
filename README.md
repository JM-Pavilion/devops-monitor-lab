# 🏴‍☠️ OverTheWire Bandit: Linux & Security Cheat Sheet

[![Python Professional CI](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml/badge.svg)](https://github.com/JM-Pavilion/devops-monitor-lab/actions/workflows/ci-test.yml)

> **Note**: This repository records my journey through the Bandit wargame, focusing on DevOps automation and Linux security. (本仓库记录了我的 Bandit 闯关之旅，侧重于 DevOps 自动化与 Linux 安全。)

---

## 🎯 Level 32: Shell Escape via $0
**Challenge**: Trapped in a restricted shell that only allows uppercase commands.
**Solution**: Use the positional parameter `$0` to spawn a new, unrestricted Bash session.

* **Command**: `>> $0`
* **Result**: Successfully "escaped" to a normal shell.

---

## 🛠️ Core Command Cheat Sheet (核心命令速查表)

### 📂 Scenario 1: Probing and Opening the Door (文件系统导航)
* `ls`: Check the contents of the current folder. (查看当前文件夹内容)
* `ls -a`: View all files, including hidden ones starting with `.`. (查看所有文件，包括隐藏文件)
* `cd <dir>`: Enter the specified folder. (进入指定文件夹)
* `file ./*`: Use "X-ray" on all files to distinguish data from human-readable ASCII text. (给文件夹里的所有文件“照X光”，分辨数据与文本)

### 📖 Scenario 2: Violent Reading (处理奇葩文件名)
* **Spaces in filenames**: Type the first few letters, then press `Tab` to autocomplete, or use `cat *` with an asterisk. (带空格的文件：输入前几个字母按 Tab 键补全，或用星号全选)
* **Files starting with `-`**: You must add `./` to tell the system this is a path (e.g., `cat ./-file01`). (以 - 开头的文件：必须加 ./ 告诉系统这是路径)

### 🔍 Scenario 3: Sea Fishing for Needles (神级搜索工具)
* `find . -size 1033c`: Find files by exact size. (按大小全盘雷达搜索)
* `find / -user bandit7 -group bandit6`: Search by permission/owner. (按权限/主人搜索)
* `grep "millionth" data.txt`: "Text Microscope" to extract specific lines from a file. (文本显微镜：精准提取特定词的行)

### ⚙️ Scenario 4: Data Cleaning Assembly Line (数据清洗流水线)
1. `sort <file>`: Sort in alphabetical order. (按字母顺序排序)
2. `uniq -u`: Delete duplicate lines and leave only unique ones. (删除重复行，只留独一无二的行)
3. **Golden Combination**: `sort data.txt | uniq -u` (sort first, then find the only one). (黄金组合技：先排序，再找唯一)

---

## 🧙 Scenario 5: Hacker's "Magic Symbols" (黑客的“魔法符号”)

| Symbol | Function (作用) | Advanced Usage (进阶用法) |
| :--- | :--- | :--- |
| `\|` | **Pipe**: Feed output to the next command. (管道符：传递结果) | Complex interaction with `mkfifo`. |
| `>` | **Overwrite**: Replace the original file. (覆盖写) | Use `tee` to read while writing. |
| `>>` | **Append**: Add to the end without destroying content. (追加写) | `tee -a` is also applicable. |
| `2>/dev/null` | **Error Black Hole**: Block unauthorized error reports. (错误黑洞) | A must-have for penetration searches. |
| `&` | **Background Operation**: Don't occupy the current screen. (后台运行) | Use `tmux` or `bg/fg` for advanced use. |
| `$( )` | **Command Replacement**: Execute inner command first. (命令替换) | Modern and readable alternative to backticks. |

---

## 🛡️ Advanced Penetration Scenes (进阶渗透场景)
* **Encrypted Communication (Level 15-16)**: Ordinary `nc` can't read encrypted data; use `openssl s_client -connect [host]:[port]` to add a "translator" layer.
* **Bypass Shell Limit (Level 18)**: When `.bashrc` kicks people, follow the command directly after SSH: `ssh user@host 'cat readme'`.
* **Git Archaeology**: Use `git log -p` to view historical differences, and `git branch -a` to find leaked keys. (Git 考古：查看历史差异与分叉支寻找密钥)

## 🐳 Cloud & DevOps Lab (云与 DevOps实验室)
- **My First Container (我的第一个容器)**: Successfully deployed and managed an Nginx web server using Docker.  (使用 Docker 成功部署并管理了Nginx Web服务器)
- **Key Commands Mastered (掌握关键命令)**: `docker run`, `docker ps`, `docker stop`.

## 🐳 Docker & Cloud Deployment (Docker 与云端部署实战)

* **Custom Image Iteration (自定义镜像迭代):** Containerized my Bandit Cheat Sheet with version control. (将速查表容器化并实现版本迭代管理)
* **v1.0:** Initial deployment using standard Nginx. (基于标准 Nginx 的初步部署)
* **v2.0:** Enhanced "Hacker Style" UI with lightweight Alpine base. (采用“黑客风格” UI 及轻量级 Alpine 镜像优化)
* **DevOps Workflow (DevOps 工作流):** Mastered `Dockerfile` crafting, image tagging, and public hosting on Docker Hub. (掌握了 Dockerfile 编写、镜像标签管理及 Docker Hub 公开托管)

### 🌐 Live Demo (实时演示)
Run my latest "Hacker Style" cheat sheet with one command:
(通过以下命令直接运行我最新的“黑客风”速查表：)
```bash```
docker run -d -p 8888:80 jminng/jm-bandit-web:v2

## 🏗️ Docker Compose & Orchestration (容器编排实战)

* **Infrastructure as Code (基础设施即代码):** Orchestrated a multi-container environment using `docker-compose`. (利用 Docker Compose 实现了多容器环境的一键编排与部署。)
* **Service Coordination (服务协同):** Successfully deployed a dual-service stack (Web App + Hello Service) with isolated networking. (成功部署了包含 Web 应用和欢迎服务的双机编队，并实现了独立的容器网络连接。)
* **Resilience (韧性能力):** Demonstrated the ability to troubleshoot network timeouts and pivot to lightweight images. (展现了排查网络超时并快速切换轻量化镜像的实战应对能力。)

### 🚀 One-Click Deployment (一键部署)
To spin up my full environment, simply run:
(只需一行命令即可启动我的完整环境：)
```bash```
docker-compose up -d

## 💾 Data Persistence & Bind Mounts (数据持久化实战)

* **Bind Mount Implementation (绑定挂载):** Decoupled static assets from the container image using Docker Volumes. (通过数据卷实现了静态资源与容器镜像的分离。)
* **Hot Reloading (热部署):** Enabled real-time UI updates without rebuilding images, significantly boosting development efficiency. (实现了无需重构镜像的实时 UI 更新，显著提升了开发效率。)
* **Storage Reliability (存储可靠性):** Ensured data persistence across container lifecycles, a foundational step toward stateful AI applications. (确保了数据在容器生命周期外的持久化存储，这是迈向有状态 AI 应用的基础。)

### 🛠️ Lab Structure (实验架构)
```test
.
├── docker-compose.yml  # The Commander (指挥官)
└── html/               # Persistent Storage (持久化存储层)
    └── index.html      # Live Content (动态内容)
```

## 🌐 Secure Internal Networking (内部网络安全实战)

* **Service Discovery (服务发现):** Confirmed that containers can communicate using service names (e.g., `ping hello`) instead of static IPs. (验证了容器间可以通过服务名互相发现，彻底告别死板的 IP 配置。)
* **Network Isolation (网络隔离):** Successfully hidden the `hello` service from the public internet while keeping it accessible to `my-web`. (成功实现了服务的内外隔离：外部无法访问，内部畅通无阻。)
* **Live API Simulation (动态请求仿真):** Observed dynamic `Request ID` updates through internal `curl` requests, simulating a real-world microservices API environment. (通过内部 curl 请求观察到了动态 ID 更新，模拟了真实的微服务 API 环境。)

## 🤖 Automated "Jarvis-Bot" (自动化特工实战)

* **Cross-Container Scripting:** Deployed a Python-based bot within the internal Docker network. (在 Docker 内网部署了 Python 特工脚本。)
* **Automated Data Extraction:** Successfully captured dynamic `Request ID` from the isolated `hello` service using regex. (利用正则匹配，自动从隔离的 hello 服务中抓取了动态 ID。)
* **Flexible Environment:** Adapted to network constraints by "side-loading" Python into an existing Alpine-based image. (巧妙利用 Alpine 镜像环境安装 Python，成功绕过 Docker Hub 下载限制。)

## ​📺 Service Monitor Dashboard (服务实时监控面板)

* **Automated Health Monitoring (自动化监控实战):** Implemented a 7x24 Python-based "Sentry" to poll service status every 5 seconds. (编写了基于 Python 的自动化“哨兵”，实现了每 5 秒一次的服务状态轮询。)
* **Visual Feedback & ANSI Colors (视觉反馈与色彩增强):** Integrated ANSI escape codes to provide immediate visual cues for system health (Green for OK, Red for Error). (集成 ANSI 转义码，通过颜色实时区分系统健康度：绿色代表正常，红色代表故障。)
* **Persistent Logging (日志持久化):** Synchronized internal container logs to the host machine for post-incident analysis. (将容器内部日志实时同步至宿主机，确保在事故发生后可进行数据追溯。)

## 🛠️ Lab Structure (实验架构)
```test
.
├── docker-compose.yml # The Commander (指挥官)
├── monitor.log        # Persistent Logs (持久化日志流)
├── bot.py             # The Sentry & Web Engine (哨兵与网页引擎)
└── html/              # Static Assets (静态资源层)
```

## 🚨 Incident Simulation & Recovery (生产事故模拟与自愈)

* ​**Service Downtime Simulation (模拟服务宕机):** Verified the monitor's alerting capability by manually stopping the hello container, observing immediate "Red" error states. (通过手动停止测试容器，验证了监控系统在秒级内触发红色报警的能力。)
* **Automated Status Recovery (服务状态自愈检测):** Confirmed the probe's ability to automatically resume "Green" status upon service restoration without manual intervention. (确认了探针在服务恢复后，无需人工干预即可自动回归绿色健康状态。)
* **​Optimized Alpine Tooling (Alpine 镜像环境优化):** Solved package installation bottlenecks by implementing Aliyun mirrors within the container startup command. (通过在启动指令中动态注入阿里云镜像源，解决了 Alpine 环境下依赖安装缓慢的问题。)

## 🔧 Version Control & Remote Sync (版本控制与云端同步实战)
* **​Git Identity Branding (Git 身份标识配置):** Standardized local environment with global user credentials to ensure professional contribution tracking. (标准化本地环境的全局用户凭证，确保所有代码贡献记录的专业追踪。)
* **​Remote Repository Linking (远程仓库关联):** Successfully established a secure bridge between the local dev environment and GitHub via remote add origin. (通过远程仓库关联指令，成功在本地开发环境与 GitHub 之间建立了安全的连接桥梁。)
* **Clean History Management (整洁历史管理):** Mastered the use of git commit --amend and --force push to maintain a high-quality, streamlined project timeline. (掌握了提交修正与强制推送技术，确保了项目时间线的简洁与高质量。)

## 🔖 Versioning & Release Management (版本发布管理实战)
* **Milestone Tagging (里程碑标签):** Leveraged Git Tags to create v1.0.0, marking the first stable deployment of the monitoring system. (利用 Git 标签创建了 v1.0.0 版本，标记了监控系统的首次稳定部署。)
* **Release Documentation (发布文档撰写):** Published formal release notes on GitHub to track feature updates and system stability. (在 GitHub 上发布了正式的 Release Notes，用于追踪功能更新与系统稳定性。)

## ​🤖 CI/CD Automation (持续集成自动化实战)
* **GitHub Actions Integration (GitHub Actions 集成):** Implemented an automated CI pipeline to perform syntax validation on every push. (实现了自动化 CI 流水线，在每次代码推送时自动进行语法校验。)
* **​Cloud Execution Environment (云端运行环境):** Configured temporary Ubuntu runners to ensure code consistency across different environments. (配置了临时的 Ubuntu 运行节点，确保代码在不同环境下的一致性。)
* **Early Bug Detection (早期错误发现):** Automated the py_compile process to catch syntax errors before manual deployment. (通过自动化编译检查，在人工部署前拦截语法错误。)

## ​🐳 Containerization & Port Mapping (容器化与端口映射实战)
* **Dockerfile Engineering:** Created a custom Python-slim image to encapsulate the monitoring environment. (创建了自定义 Python 轻量化镜像，封装了完整的监控环境。)
* **Port Forwarding Mastery:** Successfully implemented port mapping (8085:80) to demonstrate network isolation between host and container. (成功实现端口转发，演示了宿主机与容器间的网络隔离。)
* **Local Runtime Validation:** Verified the integrity of the built image by deploying a standalone container instance. (通过部署独立的容器实例，验证了构建镜像的完整性。)

# 🚀 Network Monitor v2.0

---

This is a full-network service monitoring system based on Python Flask and Docker. It can monitor the operation status of internal Docker network services and external Internet factories at the same time.    (这是一个基于 Python Flask 和 Docker 的全网服务监控系统。它能够同时监控内部 Docker 网络服务以及外部互联网大厂的运行状态。)

## ✨ Functional characteristics(功能特性)
- **Real-time monitoring(实时监控)**：Automatically check the response status of the target service every second.  (每秒自动检查目标服务的响应状态。)
- **Multi-dimensional detection(多维度探测):** Support internal container services (such as `hello`) and external websites (such as `Baidu`, `GitHub`).  (支持内部容器服务（如 `hello`）和外部网站（如 `Baidu`, `GitHub`）。)
- **Container deployment(容器化部署):** One-click start through Docker Compose, environment zero configuration.  (通过 Docker Compose 一键启动，环境零配置。)

## 🛠️ Technical stack (技术栈)
- **Language**: Python 3.9
- **Framework**: Flask (Web 界面展示)
- **Library**: Requests (网络请求), Threading (多线程并行监控)
- **Infrastructure**: Docker, Docker Compose, GitHub Actions (CI)

## 🚀 Quick start (快速启动)
1. Make sure that Docker and Docker Compose are installed.  (确保已安装 Docker 和 Docker Compose。)
2. **Run in the root directory(在根目录运行):**
   ```bash
   docker-compose up --build -d
   ```


## 🛡️ Quality Assurance (质量保证)

### **Automated Testing & CI (自动化测试与持续集成)**
This project uses **GitHub Actions** to implement a robust CI pipeline. Every time code is pushed, the system automatically:(本项目使用 **GitHub Actions** 实现了健壮的 CI 流水线。每当代码推送时，系统会自动：)
- Sets up a Python 3.9 environment.(搭建 Python 3.9 环境。)
- Installs all necessary dependencies (`flask`, `requests`, `pytest`).(安装所有必要依赖)
- Runs automated test suites to verify URL formats and service integrity.(运行自动化测试套件，校验 URL 格式及服务完整性。)
- **Goal(目标)**: Prevent human errors (like malformed URLs) from reaching production.(防止人为错误（如错误的 URL 格式）进入生产环境。)

### **Test Coverage (测试覆盖范围)**
- **URL Validation(URL 校验)**: Ensures monitoring targets start with `http` and do not contain trailing dots.(确保监控目标以 `http` 开头，且末尾没有多余的点。)
- **Service Integrity(服务完整性)**: Verifies that the monitoring target list is not empty.(验证监控目标列表不为空。)


## 💡 Achievements (今日达成)
* **CI/CD Pipeline Integration(流程全线打通)**: Successfully implemented automated Linting and Testing using GitHub Actions.(通过 GitHub Actions 实现了代码推送后的自动审计（Linting）与测试（Testing）。)
* **Code Standardization(代码质量标准化)**: Introduced `flake8` for static analysis and resolved critical `F821` (undefined name) errors to meet PEP 8 standards.(引入 `flake8` 静态检查，解决了 `F821` 等逻辑错误，使项目符合工业级规范。)
* **Advanced Git Workflow(Git 高级工作流)**: Mastered `git pull --rebase` to resolve version conflicts and maintain a clean commit history.(实战演练了 `rebase` 操作，学会在本地落后于远程时如何优雅地对齐代码。)
* **Real-time Status Monitoring(自动化状态可视化)**: Configured a live **Status Badge** on the repository to provide immediate visual feedback on build health.(配置了实时更新的 **Status Badge**，实现了项目状态的直观展示。)

## 🛠️ Troubleshooting (技术痛点排查)
* **The "Environment Gap"(环境差异”陷阱)**: Identified a crash in the CI environment caused by a missing `import os`. This highlighted the importance of environment parity.(发现在本地能跑的代码在 CI 中因缺少 `import os` 报错，深刻理解了“本地 ≠ 生产”的道理。)
* **Network Connectivity(网络连接处理)**: Successfully bypassed GitHub 443 connection errors by optimizing Git proxy settings and retry logic.(通过优化 Git 代理配置和重试机制，解决了不稳定的网络推送问题。)

## 🎯 Next Steps (下一步计划)
- [ ] **Docker Image Optimization(Docker 镜像优化)**: Explore multi-stage builds to reduce image size for faster deployment.(研究多阶段构建，压缩镜像体积以提升部署效率。)
- [ ] **Enhanced Observability(增强可观测性)**: Integrate Prometheus for advanced metrics and visualization.(计划引入 Prometheus，将监控体系从简单的告警升级为多维度的指标分析。)

## 🏗️Environment Variables & Docker Config Optimization(环境变量与容器化配置优化)

**Core Progress(核心进度):**
* ✅ **Configuration Decoupling(配置解耦):** Integrated `python-dotenv` to extract monitoring intervals from source code, enabling dynamic configuration.(引入 `python-dotenv` 库，将监控频率（Interval）从代码中抽离，实现动态配置。)
* ✅ **Docker Volume Mapping(Docker 挂载实战):** Configured `env_file` and `volumes` in `docker-compose.yml`, allowing the container to synchronize with the host's `.env` file.(通过 `docker-compose.yml` 的 `env_file` 和 `volumes` 挂载，使容器能实时读取宿主机的 `.env` 配置文件。)
* ✅ **Troubleshooting(排故经验):** Resolved naming conventions for hidden files (`.env`) and fixed `exec format error` during image building on M1 Mac.(解决了 `.env` 隐藏文件命名规范问题及 M1 Mac 芯片下的镜像构建兼容性报错。)

## Technical Insights(技术心得)
In DevOps practices, "separating configuration from code" is essential for maintaining environment consistency. By leveraging environment variables, we can modify system behavior without rebuilding images, significantly enhancing deployment flexibility.
(在 DevOps 实践中，“配置与代码分离”是实现环境一致性的关键。通过环境变量，我们无需重新构建镜像即可调整系统行为，这极大地提升了部署的灵活性。)


## 📝 Introduction(项目简介)
A lightweight Python-based service monitor that tracks website availability and sends real-time alerts via Feishu (Lark) Webhooks. It features a Dockerized environment and a Flask dashboard.(一个基于 Python 的轻量级服务监控器，实时追踪网站可用性，并通过飞书机器人发送告警,支持 Docker 化部署，并自带 Flask 监控面板。)


## 🛠️ Tech Stack(技术栈)
- **Language**: Python 3.9
- **Framework**: Flask (Dashboard)
- **Deployment**: Docker & Docker Compose
- **Platform**: Render (PaaS)
- **CI/CD**: GitHub Actions


## ⚠️ Lessons Learned (Troubleshooting) / 踩坑记录与复习

### 1. Dependency Management(依赖管理)
- **Issue**: Forgetting to add `flask` or `python-dotenv` to `requirements.txt`.(忘记将"Flask"或"Python-Dotenv"添加到"Requirements.txt"。)
- **Lesson**: Even if the code is written in `bot.py`, the cloud environment will **ignore** the libraries if they aren't listed in the "shopping list" (`requirements.txt`). This leads to a `ModuleNotFoundError`.(即使代码是用"bot.py"编写的，如果库没有列在"购物清单"("Requirements.txt")中，云环境也会**忽略**这些库。这导致了"ModuleNotFoundError"。)


### 2. YAML Indentation(YAML 缩进)
- **Issue**: GitHub Actions failed due to `mapping values are not allowed`.(由于“不允许使用映射值”，GitHub操作失败。)
- **Lesson**: YAML is extremely sensitive to spaces. Never use Tabs; always use **2 spaces** for indentation.(YAML对空格非常敏感。永远不要使用制表符；缩进总是使用"2个空格"。)

### 3. CI/CD Logic(自动化测试逻辑)
- **Issue**: GitHub Actions hanging forever.(GitHub的操作将永远挂起。)
- **Lesson**: Use a `CI=true` environment variable to tell the script to exit after one loop during testing, preventing the pipeline from being blocked by the infinite `while True` loop.(在测试过程中，使用"ci=true"环境变量告诉脚本在循环一次后退出，防止管道被无限的"while true"循环阻塞。)


## 🚀 How to Deploy(如何部署)
1. Configure `FEISHU_WEBHOOK_URL` in your environment variables.(在环境变量中配置“feishu_webhook_url”。)
2. Push code to GitHub; the CI pipeline will automatically run.(将代码推送到GitHub；CI管道将自动运行。)
3. Deploy on Render using "Clear build cache & deploy" for the first time.(首次使用“清除生成缓存和部署”在渲染时进行部署。)

## How to Debug Inside Container(如何进入容器调试)
1. docker ps to find the ID.
2. docker exec -it <ID> /bin/sh to enter.
3. tail -f monitor.log to check real-time logs.

# 🚀 JM Radar Monitor v2.5 (JM 全网监控雷达)

---

## 🛠️ Tech Stack (技术栈)
- **Monitoring**: Prometheus-style log tracking & `docker stats`

## ⚠️ Debugging & Troubleshooting (踩坑与性能调优记录)

### 1. Container File System Lock (容器文件系统锁定)
- **Issue**: Running `sed -i` inside the container on a mounted `.env` file failed with `Device or resource busy`.(在容器内对装入的".env"文件运行"sed-i"失败，原因是"设备或资源忙"。)
- **Reason**: Docker bind-mounts lock the file at the kernel level, preventing `sed` from performing its "delete-and-rename" operation.(Docker绑定挂载在内核级别锁定文件，阻止"sed"执行其"删除并重命名"操作。)
- **Solution**: Used redirection instead: `sed 's/old/new/g' .env > .env.tmp && cat .env.tmp > .env`.(改为使用重定向:“sed's/old/new/g'.env>.env.tmp&&cat.env.tmp>.env”。)

### 2. Minimal Image Tooling (极简镜像的工具缺失)
- **Issue**: Command `top` or `ps` resulted in `not found`.(命令"top"或"ps"导致"not found"。)
- **Reason**: Production-grade "Slim" images strip away non-essential binaries to reduce attack surface and image size.(生产级的“苗条”图像去除非必要的二进制文件，以减少攻击面和图像大小。)
- **Solution**: 
  - For debugging: `apt-get update && apt-get install -y procps`.
  - Best Practice: Monitored resource usage from the host using `docker stats`.(使用“Docker Stats”监控主机的资源使用情况。)

### 3. CI/CD Pipeline Blockage (流水线阻塞)
- **Issue**: GitHub Actions hung indefinitely during the test phase.(在测试阶段，GitHub的操作会无限期地暂停。)
- **Reason**: The infinite `while True` loop in the main script blocked the CI process.(主脚本中的无限“while true”循环阻塞了CI进程。)
- **Solution**: Implemented a `CI` environment variable check to force the script to exit after one successful loop in testing environments.(实现了一个“CI”环境变量检查，以强制脚本在测试环境中成功循环一次后退出。)

## 🚀 How to Run (如何运行)
1. Configure your Webhook URL in `.env`.
2. Run `docker-compose up -d`.
3. Access Dashboard at `http://localhost:80`.
4. Debug via `docker exec -it <container_id> /bin/sh`.


---

# JM's DevOps Lab: Infrastructure as Code (Terraform + LocalStack) / (实验室：基础设施即代码实战)


### 🚀 Project Overview(项目概览)
This project demonstrates the deployment of a full-stack AWS infrastructure on a local environment using **Terraform** and **LocalStack**. It mimics a real-world cloud environment without incurring any costs.(本项目展示了如何使用 **Terraform** 和 **LocalStack** 在本地环境部署全套 AWS 基础设施。它模拟了真实云环境，且不会产生任何费用。)


### 🛠️ Tech Stack(技术栈)
- **IaC Tool**: Terraform
- **Cloud Simulator**: LocalStack (Docker)
- **Cloud Provider**: AWS (Mocked)
- **OS**: Amazon Linux 2 (Simulated)

### 🏗️ Architecture Components(架构组件)
The Terraform configuration includes(Terraform 配置包含以下内容):
1. **VPC**: A custom Virtual Private Cloud with CIDR `10.0.0.0/16`.(自定义虚拟私有云，网段为 `10.0.0.0/16`。)
2. **Subnet**: A public subnet configured in `ap-southeast-1a`.(位于新加坡 A 区的公有子网。)
3. **Internet Gateway**: Enabling internet connectivity for the VPC.(为 VPC 开启互联网连接的网关。)
4. **Route Table**: Configuring traffic routing to the IGW.(配置通往互联网网关的路由条目。)
5. **Security Group**: Firewall rules allowing SSH (22) and HTTP (80) traffic.(防火墙规则，允许 SSH (22) 和 HTTP (80) 流量。)
6. **EC2 Instance**: A virtual machine running with a dynamically fetched AMI.(使用动态获取的 AMI 镜像启动的虚拟机。)

### 📖 Key Learnings / 核心收获
- Mastered the **Terraform Workflow** {`init`, `plan`, `apply`, `destroy`}.(掌握了 **Terraform 工作流**（初始化、计划、应用、销毁）。)
- Learned to handle **Resource Dependencies** and **Data Sources**.(学习了如何处理**资源依赖**和**动态数据源**。)
- Practiced **Infrastructure Troubleshooting** (debugging AMI ID mismatches)./(练习了**基础设施排错**（调试 AMI ID 不匹配问题）。)

*Created by JM as part of the 2026-2027 Career Sprint.*

---

## 🚀 Step 1: Containerized Infrastructure Deployment(容器化基础设施部署) (2026-04-09)

### In this iteration, we focused on "drilling down" into the end-to-end deployment workflow(在本次迭代中，我们成功实现了监控系统的“降速打穿”学习，完成了从基础设施自动化到应用容器化的全链路部署：):
* **Infrastructure Enhancement(基础设施增强)**: Optimized AWS Security Groups via Terraform, exposing Port 80 for Web traffic and implementing Nginx persistence using `user_data`.(使用 Terraform 优化了 AWS 安全组配置，开放 80 端口用于 Web 服务，并通过 `user_data` 实现了 Nginx 的自启动管理。)
* **Containerization(应用容器化)**: Built a custom Docker image, applying the "pre-packaged meal" concept to ensure environmental consistency.(编写并构建了 Docker 镜像（Image），通过“预制菜”理念解决环境一致性问题。)
* **Network Troubleshooting(网络链路优化)**: Resolved port mismatch issues (Host 5001 to Container 10000) and updated Flask binding from `127.0.0.1` to `0.0.0.0` for external accessibility.(解决了容器内外端口映射不匹配（10000 vs 5001）以及 Flask 在 Docker 内的监听地址问题（从 127.0.0.1 转向 0.0.0.0）。)
* **Multi-device Verification(多端验证)**: Verified accessibility across both desktop and mobile devices within the same local network.(实现了同一局域网下移动端与 PC 端的同步访问验证。)


## 🤖 Step 2: Automated CI Pipeline with GitHub Actions(使用 GitHub Actions 构建自动化 CI 流水线) (2026-04-10)

### Successfully implemented a fully automated Continuous Integration (CI) workflow(今天成功打通了从“代码提交”到“镜像入库”的全自动化流程 (CI)):
* **Security Management(安全管理)**: Configured Docker Hub credentials in GitHub Secrets using Personal Access Tokens (PAT) instead of plain-text passwords, adhering to the principle of least privilege.(在 GitHub Secrets 中配置了 Docker Hub 凭据，通过 Personal Access Token (PAT) 代替明文密码，遵循最小权限原则。)
* **Pipeline Automation(流水线自动化)**: Created `.github/workflows/docker-image.yml` to trigger automatic builds whenever changes are pushed to the `main` branch.(编写了 `.github/workflows/docker-image.yml`，实现了基于 `main` 分支推送触发的自动构建。)
* **Image Registry(镜像托管)**: Successfully pushed the Docker image to a cloud registry (Docker Hub), eliminating local environment dependencies and paving the way for Continuous Deployment (CD) on AWS.(成功将打包好的 Docker 镜像推送到云端仓库 (Docker Hub)，消除了本地环境依赖，为下一步的云端部署 (CD) 打下坚实基础。)


## ☁️ Step 3: Simulated Cloud Deployment with LocalStack(使用 LocalStack 进行模拟云端部署) (2026-04-11)

### Successfully simulated the Continuous Deployment (CD) pipeline in a production-like environment(今天成功模拟了生产环境的持续部署 (CD) 流程):
* **Environment Adaptation(环境变通)**: Utilized LocalStack as an AWS cloud emulator to validate Infrastructure-as-Code (IaC) logic under credential constraints.(由于真实 AWS 账户权限限制，采用了 LocalStack 作为云端模拟器，成功验证了基础设施即代码 (IaC) 的逻辑。)
* **Container Lifecycle(容器化闭环)**: Manually pulled the `jminng/jm-monitor:latest` image, which was automatically built and pushed by GitHub Actions.(手动拉取了由 GitHub Actions 自动生成的 `jminng/jm-monitor:latest` 镜像。)
* **Service Exposure(端口映射与上线)**: Configured port mapping (`8080:10000`) between the container and host, successfully replicating cloud-based public access and verifying service health.(实现了容器与宿主机的端口转发 (`8080:10000`)，成功在本地模拟了云端公网访问的效果，验证了服务的可用性。)
