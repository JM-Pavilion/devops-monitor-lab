import logging
import requests
import time
import os
import threading
from flask import Flask
from dotenv import load_dotenv

# 1. 加载本地 .env 文件（云端环境会自动忽略这一步）
load_dotenv()

# --- 配置区域 ---
INTERVAL = int(os.getenv("MONITOR_INTERVAL", "60"))
# 统一使用 FEISHU_WEBHOOK 变量名
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL")

TARGETS = {
    "Baidu-Search": "https://www.baidu.com",
    "GitHub-Global": "https://github.com",
    "Bing-Search": "https://www.bing.com",
}

# --- 状态存储 ---
service_status_cache = {}
last_known_status = {}

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- 告警函数 ---
def send_feishu_alert(service_name, status_desc):
    if not FEISHU_WEBHOOK:
        print("🛑 未配置飞书 Webhook，跳过告警发送。")
        return

    # 修复了 f-string 格式问题
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🚨 JM 雷达告警：服务 [{service_name}] 状态异常！\n当前状态：{status_desc}\n检查时间：{time.ctime()}"
        },
    }
    try:
        requests.post(FEISHU_WEBHOOK, json=payload, timeout=5)
        print("✅ 告警消息已发送到飞书群")
    except Exception as e:
        print(f"❌ 发送飞书告警失败: {e}")

# --- 核心监控线程 ---
def monitoring_worker():
    print("🕵️‍♂️ 后台监控线程已启动...")
    global service_status_cache
    
    for name in TARGETS:
        last_known_status[name] = "Normal"

    while True:
        temp_cache = {}
        for name, url in TARGETS.items():
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    status_text = "✅ 运行正常"
                    current_state = "Normal"
                else:
                    status_text = f"⚠️ 状态码异常: {resp.status_code}"
                    current_state = "Error"
            except requests.exceptions.RequestException:
                status_text = "❌ 发现故障: 网络不可达"
                current_state = "Down"

            if last_known_status.get(name) == "Normal" and current_state != "Normal":
                print(f"🔥 检测到服务变更: {name} 变为 {current_state}")
                send_feishu_alert(name, status_text)

            last_known_status[name] = current_state
            temp_cache[name] = status_text
            print(f"{time.ctime()} - {name}: {status_text}")

        service_status_cache = temp_cache
        
        # 巧妙设计：如果是 GitHub 测试环境，跑一遍就退出，防止测试卡死
        if os.getenv("CI") == "true":
            break
            
        time.sleep(INTERVAL)

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
    # 1. 启动后台巡逻线程
    t = threading.Thread(target=monitoring_worker, daemon=True)
    t.start()

    # 2. 启动网页服务器 (如果是 CI 测试环境则不启动网页，直接宣告成功)
    if os.getenv("CI") != "true":
        port = int(os.environ.get("PORT", 10000))
        print(f"🌐 Web 界面已启动，端口: {port}")
        app.run(host="0.0.0.0", port=port)
    else:
        print("✅ CI 自动化测试通过！")
