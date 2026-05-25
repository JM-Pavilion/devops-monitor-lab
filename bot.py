import json
import logging
import requests
import time
import os
import threading
import sys
import random
from flask import Flask, render_template, jsonify, request  # ✨ 确保里面有 request！
from dotenv import load_dotenv

load_dotenv()

# --- 1.初始化全局变量（防止 Flask 报错）---
service_status_cache = {}
last_known_status = {}
app = Flask(__name__)

# --- 2.配置区域 ---
INTERVAL = int(os.getenv("MONITOR_INTERVAL", "20"))
# 统一使用 FEISHU_WEBHOOK 变量名
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL")
# ---1.动态加载配置文件 ---
CONFIG_FILE = "config.json"

# --- 3.日志配置 ---
# 优先读取环境变量 LOG_PATH，如果读不到，默认用绝对路径 /app/logs
LOG_DIR = os.getenv("LOG_PATH", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)
log_format = '%(asctime)s - %(message)s'
log_file = os.path.join(LOG_DIR, 'monitor.log')

# --- 3.同时输出到控制台和文件 ---
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
LATENCY_THRESHOLD = config.get("TIMEOUT_THRESHOLD_MS", 1500) / 1000.0 # 转换为秒
TARGETS = config.get("TARGETS", {})

# ---2. 全局状态记忆库 ---
service_status_cache = {}  # 存储最新的状态文本，用于网页展示
last_known_status = {}     # 存储上一次的状态（Normal/Error/Down），用于状态机逻辑判断

# 全局心跳内存账本
heartbeat_ledger = {
"🔥雷达自身守护锁": time.time() # 初始化雷达自己也是健康的
}

# --- 3. 飞书高级卡片升级 ---
def send_feishu_template_alert(service_name, status_desc, latency_ms=None, is_recovery=False):
    """
    发送飞书互动卡片告警：支持故障红框、恢复绿框及一键直达
    """
    if not FEISHU_WEBHOOK:
        print("🛑 未配置飞书 Webhook，跳过告警发送。")
        return

    # 动态调整卡片颜色和标题：故障用红色(red)，恢复用绿色(green)
    theme = "green" if is_recovery else "red"
    title_prefix = "🟢【恢复】" if is_recovery else "🚨【警报】"
    url = TARGETS.get(service_name, "https://www.baidu.com")

    latency_info = f"\n**响应时间**：`{latency_ms} ms`" if latency_ms else ""

    # 飞书互动卡片最新 v2 语法结构
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{title_prefix} {service_name} 状态变更"
                },
                "template": theme
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**服务名称**：`{service_name}`\n**当前状态**：{status_desc}\n**检测时间**：{time.strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "🌐 一键直达目标服务"
                            },
                            "type": "primary" if is_recovery else "danger",
                            "url": url
                        }
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
    global last_known_status # 强行给机器人灌入记忆功能，不准它失忆！
    
    # 初始化：让机器人记住所有网站最初都是正常（Normal）
    for name in TARGETS:
        if name not in last_known_status:
            last_known_status[name] = "Normal"

    while True:
        # 每次循环都重新加载配置文件，支持热更新（修改 config.json 后无需重启）
        current_config = load_config()
        current_targets = current_config.get("TARGETS", {})
        current_threshold = current_config.get("TIMEOUT_THRESHOLD_MS", 1500) / 1000.0

        temp_cache = {}

        # ==========================================
        # 🔍 第一阶段：主动出击轮询（HTTP 探针）
        # ==========================================
        for name, url in current_targets.items():
            start_time = time.time() # 开始计时
            try:
                resp = requests.get(url, timeout=10)
                latency = time.time() - start_time # 计算耗时（秒）
                latency_ms = int(latency * 1000) # 转换为毫秒

                if resp.status_code == 200:
                    # ✨【Phase 4 核心进化】：如果是我们自己的微服务，进行深度业务码探针检测
                    if "/api/" in url:
                        try:
                            business_data = resp.json()  # 🔍 强行解剖 JSON 内脏
                            b_code = business_data.get("code")
                            if b_code == 20000:
                                status_text = f"✅ 业务正常 (用户数: {business_data['data']['active_users']})"
                                current_state = "Normal"
                            else:
                                status_text = f"❌ 业务内伤！错误码: {b_code}, 原因: {business_data.get('message')}"
                                current_state = "BusinessError"
                        except Exception:
                            status_text = "⚠️ 接口虽通，但返回的不是合法的 JSON 数据！"
                            current_state = "FormatError"
                    else:
                        # 普通的外部网站，依然走原来的延迟检测逻辑
                        if latency > current_threshold:
                            status_text = f"⚠️ 勉强可用，但延迟极高！"
                            current_state = "HighLatency"
                        else:
                            status_text = "✅ 运行正常"
                            current_state = "Normal"
                else:
                    # ✨【修复点 1】：补回被误删的非 200 异常状态码处理
                    status_text = f"⚠️ 状态码异常: {resp.status_code}"
                    current_state = "Error"

            except requests.exceptions.RequestException:
                # ✨【修复点 2】：补回被连根挖掉的外层网络异常捕获
                status_text = "❌ 发现故障: 网络不可达"
                current_state = "Down"
                latency_ms = None # 故障时不显示延迟

            # 【核心状态机锁逻辑】
            previous_state = last_known_status.get(name, "Normal")

            # 情况A：原本正常，现在异常了 → 发送红色告警卡片
            if previous_state == "Normal" and current_state != "Normal":
                send_feishu_template_alert(name, f"{status_text}", latency_ms, is_recovery=False)
            
            # 情况B：原本异常，现在恢复了 → 发送绿色恢复卡片
            elif previous_state != "Normal" and current_state == "Normal":
                send_feishu_template_alert(name, "服务已恢复健康运行", latency_ms, is_recovery=True)

            # 更新记忆状态，其余“持续挂着”或“持续正常”的情况不发送告警，只更新状态
            last_known_status[name] = current_state
            temp_cache[name] = f"{status_text} ({latency_ms}ms)" if latency_ms else status_text
            print(f"[{time.strftime('%X')}] {name}: {status_text} ({latency_ms if latency_ms else 'N/A'} ms)")

        # ==========================================
        # 💓 第二阶段：大本营守株待兔（被动心跳审查）
        # ==========================================
        now = time.time()
        heartbeat_threshold = 30 # 超过30秒没收到心跳就认为服务挂了
        for s_name, last_seen in list(heartbeat_ledger.items()):
            elapsed_time = int(now - last_seen)
            prev_state = last_known_status.get(s_name, "Normal")

            if elapsed_time > heartbeat_threshold:
                # 判定为失联
                status_text = f"❌ 失去心跳联络！已持续失联 {elapsed_time} 秒！"
                current_state = "HeartbeatLost" # ✨【修复点 2】：修正拼写错误

                # 状态机锁：只有从正常变成异常时，才发飞书红色高级卡片
                if prev_state == "Normal":
                    send_feishu_template_alert(s_name, status_text, latency_ms=None, is_recovery=False)

                last_known_status[s_name] = "HeartbeatLost"
                temp_cache[s_name] = f"💀 心跳失联 ({elapsed_time}s)"
            else:
                # 依然健康存活
                status_text = "✅ 心跳保持中"
                current_state = "Normal"

                # 状态机锁：只有从异常恢复到正常时，才发飞书绿色高级卡片
                if prev_state != "Normal":
                    send_feishu_template_alert(s_name, "服务心跳已恢复正常上报", latency_ms=None, is_recovery=True)
                
                last_known_status[s_name] = "Normal"
                temp_cache[s_name] = f"💓 存活中 (最近一次：{elapsed_time}s前)"

            # 核心补丁：吧心跳状态也大声喊出来打印在终端上！
            print(f"[{time.strftime('%X')}] {s_name}: {status_text} (被动心跳)")

        service_status_cache = temp_cache
        if os.getenv("CI") == "true":
            break
        time.sleep(current_config.get("MONITOR_INTERVAL",20))

# --- Flask 路由区域 ---
@app.route("/api/user-service/status")
def user_service_status():
    """
    模拟微服务的真实接口：
    80% 概率返回真正的业务大捷数据，20% 概率网络通但业务报错（触发内伤）
    """
    if random.random() < 0.2:
        # 模拟“外表健康（200 OK）但内在有病（业务错误）”的情况
        return {"status": "error", "code": 50001, "message": "Database Connection Timeout!"}, 200
    
    # 正常情况
    return {"status": "success", "code": 20000, "data": {"active_users": 1024, "db_status": "HEALTHY"}}, 200

@app.route("/api/heartbeat", methods=["POST"])
def receive_heartbeat():
    """接收各大微服务主动上报的心跳信号"""
    try:
        # 强制解析，防止终端 curl 的单双引号引发崩溃
        data = request.get_json(force=True, silent=True) 
        if not data:
            return {"status": "error", "message": "Invalid JSON format"}, 400
            
        service_name = data.get("service_name")
        if not service_name:
            return {"status": "error", "message": "Missing service_name"}, 400
        
        # 🧾 在账本上更新时间戳
        global heartbeat_ledger
        heartbeat_ledger[service_name] = time.time()
        
        print(f"🎯 [API] 成功接收到来自 [{service_name}] 的复活心跳包！")
        return {"status": "success", "message": f"Heartbeat received!"}, 200
    except Exception as e:
        print(f"❌ [API] 心跳接口崩溃: {e}")
        return {"status": "error", "message": str(e)}, 500


# --- Flask Web 界面 ---
@app.route("/")
def index():
    status_cards = ""
    for name, status in service_status_cache.items():
        # 修正颜色和逻辑
        is_ok = "✅" in status
        bg_color = "bg-green-100 border-green-500 text-green-700" if is_ok else "bg-red-100 border-red-500 text-red-700"
        
        # 修正 ping_dot 字符串拼接
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

    # --- 重要：这里的 return 必须跟 if 对齐，确保无论如何都会返回 HTML ---
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="5">
            <script src="https://cdn.tailwindcss.com"></script>
            <title>JM Radar Dashboard</title>
            <style>
                @keyframes pulse-soft {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.7; }}
                }}
                .animate-pulse-soft {{ animation: pulse-soft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
            </style>
        </head>
        <body class="bg-slate-900 text-slate-100 p-8">
            <div class="max-w-5xl mx-auto">
                <header class="flex justify-between items-end mb-12 border-b border-slate-700 pb-6">
                    <div>
                        <h1 class="text-5xl font-black tracking-tight text-white">
                            JM <span class="text-blue-500">RADAR</span>
                        </h1>
                        <p class="text-slate-400 mt-2 font-mono uppercase tracking-widest text-xs">Cloud Infrastructure Monitoring</p>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-slate-500 font-mono">SYSTEM STATUS: <span class="text-green-400">ACTIVE</span></div>
                        <div class="text-xs text-slate-500 font-mono">INTERVAL: {INTERVAL}s</div>
                    </div>
                </header>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {status_cards}
                </div>

                <footer class="mt-16 pt-8 border-t border-slate-800 flex justify-between items-center text-slate-500 text-xs font-mono">
                    <div>© 2026 JM DEVOPS LAB</div>
                    <div>LAST SCAN: {time.strftime('%H:%M:%S')}</div>
                </footer>
            </div>
        </body>
    </html>
    """

# --- 主程序入口 ---
if __name__ == "__main__":
    # 如果是 CI 环境：直接跑一次逻辑，不启动网页，也不用开多线程
    if os.getenv("CI") == "true":
        print("⚠️ CI mode detected: Executing a single check for validation...")
        # 直接调用你的函数（不要在后台线程跑，就在当前跑完它）
        monitoring_worker()
        print("✅ CI 自动化测试通过！")
        import sys
        sys.exit(0)

    # 在 Flask 启动之前执行，这样一开机就能看到！快点
    print("==================================================")
    print("🔥 5-18 捷报：JM-Monitor 工业级流水线全自动热更新成功！🔥")
    print("==================================================")

    # 如果是正常环境：启动后台线程 + 启动 Flask
    t = threading.Thread(target=monitoring_worker, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    # 2026-05-07 最后的加固测试
    print("Web Server Started at port: {}".format(port))
    # print(f"🌐 Web 界面已启动，端口: {port}")
    app.run(host="0.0.0.0", port=port)


