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

## 🚀 Network Monitor v2.0

This is a full-network service monitoring system based on Python Flask and Docker. It can monitor the operation status of internal Docker network services and external Internet factories at the same time.    (这是一个基于 Python Flask 和 Docker 的全网服务监控系统。它能够同时监控内部 Docker 网络服务以及外部互联网大厂的运行状态。)

### ✨ Functional characteristics(功能特性)
- **Real-time monitoring(实时监控)**：Automatically check the response status of the target service every second.  (每秒自动检查目标服务的响应状态。)
- **Multi-dimensional detection(多维度探测):** Support internal container services (such as `hello`) and external websites (such as `Baidu`, `GitHub`).  (支持内部容器服务（如 `hello`）和外部网站（如 `Baidu`, `GitHub`）。)
- **Container deployment(容器化部署):** One-click start through Docker Compose, environment zero configuration.  (通过 Docker Compose 一键启动，环境零配置。)

### 🛠️ Technical stack (技术栈)
- **Language**: Python 3.9
- **Framework**: Flask (Web 界面展示)
- **Library**: Requests (网络请求), Threading (多线程并行监控)
- **Infrastructure**: Docker, Docker Compose, GitHub Actions (CI)

### 🚀 Quick start (快速启动)
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





