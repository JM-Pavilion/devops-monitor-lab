import json
import logging
import requests
import time
import os
import threading
import sys
import random
# ✨ 引入 Response，用于输出标准的 Prometheus 时序文本
from flask import Flask, render_template, jsonify, request, Response  
from dotenv import load_dotenv

# ✨ 重新注入云原生核心监控库
from prometheus_client import generate_latest, Counter, Gauge

load_dotenv()

# --- 1.初始化全局变量与 Flask 实例 ---
service_status_cache = {}
last_known_status = {}
app = Flask(__name__)

# --- ✨ 重新注入 Prometheus 核心监控指标定义 ---
HTTP_REQUESTS_TOTAL = Counter('jm_monitor_http_requests_total', 'Total HTTP Requests Caught', ['endpoint'])
SERVICE_STATUS_GAUGE = Gauge('jm_monitor_service_status', 'Service Status (1=OK, 0=Error)', ['service_name'])

# --- 2.配置区域 ---
INTERVAL = int(os.getenv("MONITOR_INTERVAL", "20"))
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# --- 3.日志配置 ---
LOG_DIR = os.getenv("LOG_PATH", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)
log_format = '%(asctime)s - %(message)s'
log_file = os.path.join(LOG_DIR, 'monitor.log')

logging.basicConfig(level=logging.INFO, format=log_format, handlers=[
    logging.FileHandler(log_file),
    logging.StreamHandler()
])

logging.info("🚀 监控服务已启动，日志记录开始...")

def load_config():
    """动态读取 JSON 配置文件"""
    default_config = {
        "MONITOR_INTERVAL": 20,
        "TIMEOUT_THRESHOLD_MS": 1500,
        "TARGETS": {
            "百度首页": "https://www.baidu.com",
            "GitHub主站": "https://github.com",
            "bing搜索": "https://www.bing.com"
        }
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 读取 config.json 失败，使用默认配置: {e}")
    return default_config

config = load_config()
INTERVAL = config.get("MONITOR_INTERVAL", 20)
LATENCY_THRESHOLD = config.get("TIMEOUT_THRESHOLD_MS", 1500) / 1000.0
TARGETS = config.get("TARGETS", {})

# 全局心跳内存账本
heartbeat_ledger = {
    "🔥雷达自身守护锁": time.time()
}

# --- 3. 飞书高级卡片升级 ---
def send_feishu_template_alert(service_name, status_desc, latency_ms=None, is_recovery=False):
    if not FEISHU_WEBHOOK:
        print("🛑 未配置飞书 Webhook，跳过告警发送。")
        return

    theme = "green" if is_recovery else "red"
    title_prefix = "🟢【恢复】" if is_recovery else "🚨【警报】"
    url = TARGETS.get(service_name, "https://www.baidu.com")

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"{title_prefix} {service_name} 状态变更"},
                "template": theme
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"**服务名称**：`{service_name}`\n**当前状态**：{status_desc}\n**检测时间**：{time.strftime('%Y-%m-%d %H:%M:%S')}"}
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "🌐 一键直达目标服务"}, "type": "primary" if is_recovery else "danger", "url": url}
                    ]
                }
            ]
        }
    }
    requests.post(FEISHU_WEBHOOK, json=payload, timeout=5)

# --- 4. 核心多维度监控线程 ---
def monitoring_worker():
    logging.info("🕵️‍♂️ 后台监控线程已启动...")
    global service_status_cache
    global last_known_status 
    
    for name in TARGETS:
        if name not in last_known_status:
            last_known_status[name] = "Normal"

    while True:
        current_config = load_config()
        current_targets = current_config.get("TARGETS", {})
        current_threshold = current_config.get("TIMEOUT_THRESHOLD_MS", 1500) / 1000.0

        temp_cache = {}

        # ==========================================
        # 🔍 第一阶段：主动出击轮询（HTTP 探针）
        # ==========================================
        for name, url in current_targets.items():
            start_time = time.time()
            try:
                resp = requests.get(url, timeout=10)
                latency = time.time() - start_time
                latency_ms = int(latency * 1000)

                if resp.status_code == 200:
                    if "/api/" in url:
                        try:
                            business_data = resp.json()  
                            b_code = business_data.get("code")
                            if b_code == 20000:
                                status_text = f"✅ 业务正常 (用户数: {business_data['data']['active_users']})"
                                current_state = "Normal"
                            else:
                                status_text = f"❌ 业务内伤！错误码: {b_code}"
                                current_state = "BusinessError"
                        except Exception:
                            status_text = "⚠️ 接口虽通，但返回的不是合法的 JSON 数据！"
                            current_state = "FormatError"
                    else:
                        if latency > current_threshold:
                            status_text = f"⚠️ 勉强可用，但延迟极高！"
                            current_state = "HighLatency"
                        else:
                            status_text = "✅ 运行正常"
                            current_state = "Normal"
                else:
                    status_text = f"⚠️ 状态码异常: {resp.status_code}"
                    current_state = "Error"

            except requests.exceptions.RequestException:
                status_text = "❌ 发现故障: 网络不可达"
                current_state = "Down"
                latency_ms = None

            # ✨ 核心联动：将抓取到的微服务状态，同步更新进 Prometheus 仪表盘指标
            SERVICE_STATUS_GAUGE.labels(service_name=name).set(1 if current_state == "Normal" else 0)

            previous_state = last_known_status.get(name, "Normal")
            if previous_state == "Normal" and current_state != "Normal":
                send_feishu_template_alert(name, f"{status_text}", latency_ms, is_recovery=False)
            elif previous_state != "Normal" and current_state == "Normal":
                send_feishu_template_alert(name, "服务已恢复健康运行", latency_ms, is_recovery=True)

            last_known_status[name] = current_state
            temp_cache[name] = f"{status_text} ({latency_ms}ms)" if latency_ms else status_text

        # ==========================================
        # 💓 第二阶段：被动心跳审查
        # ==========================================
        now = time.time()
        heartbeat_threshold = 30 
        for s_name, last_seen in list(heartbeat_ledger.items()):
            elapsed_time = int(now - last_seen)
            prev_state = last_known_status.get(s_name, "Normal")

            if elapsed_time > heartbeat_threshold:
                status_text = f"❌ 失去心跳联络！已持续失联 {elapsed_time} 秒！"
                current_state = "HeartbeatLost"
                SERVICE_STATUS_GAUGE.labels(service_name=s_name).set(0)

                if prev_state == "Normal":
                    send_feishu_template_alert(s_name, status_text, latency_ms=None, is_recovery=False)

                last_known_status[s_name] = "HeartbeatLost"
                temp_cache[s_name] = f"💀 心跳失联 ({elapsed_time}s)"
            else:
                status_text = "✅ 心跳保持中"
                current_state = "Normal"
                SERVICE_STATUS_GAUGE.labels(service_name=s_name).set(1)

                if prev_state != "Normal":
                    send_feishu_template_alert(s_name, "服务心跳已恢复正常上报", latency_ms=None, is_recovery=True)
                
                last_known_status[s_name] = "Normal"
                temp_cache[s_name] = f"💓 存活中 (最近一次：{elapsed_time}s前)"

        service_status_cache = temp_cache
        if os.getenv("CI") == "true":
            break
        time.sleep(current_config.get("MONITOR_INTERVAL", 20))

# --- Flask 路由区域 ---

# ✨ 核心补丁：重新把暴露给 Prometheus 抓取的官方指标通道建起来！
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8")

@app.route("/api/alert/webhook", methods=["POST"])
def grafana_webhook_translator():
    """
    ✨ 黄金翻译官：接收 Grafana 发来的原生大 JSON，翻译成精美的飞书高级卡片发出去！
    """
    try:
        # 强行捕获 Grafana 甩过来的数据包
        data = request.get_json(force=True, silent=True)
        if not data:
            print("⚠️ 收到来自 Grafana 的空警报投递")
            return {"status": "error", "message": "No data received"}, 400
        
        # 拆解大厂级告警外壳
        alert_status = data.get("status", "firing") # firing 代表警报，resolved 代表恢复
        alerts_list = data.get("alerts", [])
        
        for single_alert in alerts_list:
            labels = single_alert.get("labels", {})
            # 提取我们在 Grafana 面板里起的标题名字
            alert_name = labels.get("alertname", "Grafana 未知雷达警报")
            
            # 判断生死状态
            is_recovery = (alert_status == "resolved" or single_alert.get("status") == "resolved")
            
            if is_recovery:
                status_desc = "🟢 【恢复】流量洪峰已退去，微服务负载重回安全水位。"
            else:
                status_desc = "🚨 【爆发】QPS 并发量已严重超出预设阈值，请速去大盘排查！"
            
            # 巧妙借用我们现成的飞书卡片引擎，直接出击！
            send_feishu_template_alert(
                service_name=f"雷达立体监控 -> {alert_name}",
                status_desc=status_desc,
                latency_ms=None,
                is_recovery=is_recovery
            )
            
        print(f"🔔 [翻译官] 成功将 Grafana 的 {len(alerts_list)} 个警报翻译并成功轰炸至飞书！")
        return {"status": "success"}, 200
        
    except Exception as e:
        print(f"❌ [翻译官] 严重翻车，未能成功翻译 Grafana 警报: {e}")
        return {"status": "error", "message": str(e)}, 500

@app.route("/api/user-service/status")
def user_service_status():
    HTTP_REQUESTS_TOTAL.labels(endpoint='/api/user-service/status').inc()
    if random.random() < 0.2:
        return {"status": "error", "code": 50001, "message": "Database Connection Timeout!"}, 200
    return {"status": "success", "code": 20000, "data": {"active_users": 1024, "db_status": "HEALTHY"}}, 200

@app.route("/api/heartbeat", methods=["POST"])
def receive_heartbeat():
    HTTP_REQUESTS_TOTAL.labels(endpoint='/api/heartbeat').inc()
    try:
        data = request.get_json(force=True, silent=True) 
        if not data:
            return {"status": "error", "message": "Invalid JSON format"}, 400
        service_name = data.get("service_name")
        if not service_name:
            return {"status": "error", "message": "Missing service_name"}, 400
        
        global heartbeat_ledger
        heartbeat_ledger[service_name] = time.time()
        return {"status": "success", "message": "Heartbeat received!"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/")
def index():
    HTTP_REQUESTS_TOTAL.labels(endpoint='/').inc()
    status_cards = ""
    for name, status in service_status_cache.items():
        is_ok = "✅" in status
        bg_color = "bg-green-100 border-green-500 text-green-700" if is_ok else "bg-red-100 border-red-500 text-red-700"
        
        ping_dot = ""
        if is_ok:
            ping_dot = (
                '<span class="relative flex h-3 w-3">'
                '<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>'
                '<span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>'
                '</span>'
            )

        status_cards += f'''
        <div class="p-4 rounded-xl border-2 {bg_color} shadow-lg transition-all duration-500 hover:scale-105">
          <div class="flex justify-between items-start">
            <h2 class="font-bold text-xl">{name}</h2>
            {ping_dot}
          </div>
          <p class="text-sm mt-2 font-mono">{status}</p>
        </div>
        '''

    if not status_cards:
        status_cards = "<p class='text-gray-400'>📡 正在初始化雷达数据，请稍等几秒后刷新...</p>"

    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="5">
            <script src="https://cdn.tailwindcss.com"></script>
            <title>JM Radar Dashboard</title>
        </head>
        <body class="bg-slate-900 text-slate-100 p-8">
            <div class="max-w-5xl mx-auto">
                <header class="flex justify-between items-end mb-12 border-b border-slate-700 pb-6">
                    <div>
                        <h1 class="text-5xl font-black tracking-tight text-white">JM <span class="text-blue-500">RADAR</span></h1>
                        <p class="text-slate-400 mt-2 font-mono uppercase tracking-widest text-xs">Cloud Infrastructure Monitoring</p>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-slate-500 font-mono">SYSTEM STATUS: <span class="text-green-400">ACTIVE</span></div>
                        <div class="text-xs text-slate-500 font-mono">INTERVAL: {INTERVAL}s</div>
                    </div>
                </header>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{status_cards}</div>
                <footer class="mt-16 pt-8 border-t border-slate-800 flex justify-between items-center text-slate-500 text-xs font-mono">
                    <div>© 2026 JM DEVOPS LAB</div>
                    <div>LAST SCAN: {time.strftime('%H:%M:%S')}</div>
                </footer>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    if os.getenv("CI") == "true":
        monitoring_worker()
        sys.exit(0)

    t = threading.Thread(target=monitoring_worker, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
