import requests
import time
from flask import Flask
import os
import threading # 👈 用于开启后台巡逻线程

app = Flask(__name__)

# --- 1. 配置区域 ---

# 🎯 监控名单 (保留你原来的设置)
TARGETS = {
    "Internal-Hello-Service": "http://hello",
    "External-Baidu": "https://www.baidu.com",# 故意写错域名，测试告警功能
    "External-GitHub": "https://github.com"
}

# 🚨 飞书机器人 Webhook 地址
# 为了安全，这里使用环境变量读取。我们稍后在 Render 后台配置它。
# 如果不配置，默认为“未填”，机器人会打印日志提示你。
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK_URL")

# --- 2. 共享状态区域 ---
# 用于存储后台线程最新的监控结果，前端UI直接读取这个，速度极快
service_status_cache = {}
# 用于记录上一次的状态，检查从正常变为不正常时触发告警
last_known_status = {}

# --- 3. 告警发送函数 ---
def send_feishu_alert(service_name, status_desc):
    """当服务出问题时，给飞书发消息"""
    if FEISHU_WEBHOOK == "FEISHU_WEBHOOK_URL":
        print("🛑 [FEISHU ALERT] 未配置飞书 Webhook，跳过发送告警。")
        return

    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🚨 JM 雷达告警：服务 [{service_name}] 状态异常！\n当前状态：{status_desc}\n检查时间：{time.ctime()}"
        }
    }
    try:
        # 增加 timeout，防止告警失败卡死监控核心
        requests.post(FEISHU_WEBHOOK, json=payload, timeout=5)
        print(f"✅ [FEISHU ALERT] 告警消息已发送到飞书群")
    except Exception as e:
        print(f"❌ [FEISHU ALERT] 发送飞书告警失败: {e}")

# --- 4. 后台监控线程逻辑 ---
def monitoring_worker():
    """永不停止的后台工作线程，负责监控、写日志、触发告警"""
    print("🕵️‍♂️ 后台监控线程已启动...")
    global service_status_cache, last_known_status

    # 初始化状态，防止第一次启动乱报错
    for name in TARGETS:
        last_known_status[name] = "Normal"

    while True:
        # 在云端volume不持久化，但可以保留，供通过 SSH 登录排查
        with open("monitor.log", "a") as f:
            temp_cache = {}
            for name, url in TARGETS.items():
                try:
                    # 增加 timeout，防止单个服务卡死导致整个线程挂掉
                    resp = requests.get(url, timeout=3)
                    
                    if resp.status_code == 200:
                        status_text = "✅ 运行正常"
                        current_state = "Normal"
                    else:
                        status_text = f"⚠️ 状态码异常: {resp.status_code}"
                        current_state = "Error"
                except requests.exceptions.RequestException as e:
                    status_text = f"❌ 发现故障: 网络不可达"
                    current_state = "Down"

                # --- 核心：状态比对与告警触发 ---
                # 只有从 变成非 Normal (Error/Down) 时才触发告警
                if last_known_status.get(name) == "Normal" and current_state != "Normal":
                    print(f"🔥 检测到服务变更: {name} 从 Normal 变为 {current_state}")
                    send_feishu_alert(name, status_text)

                # 更新记录状态
                last_known_status[name] = current_state
                temp_cache[name] = status_text
                f.write(f"{time.ctime()} - {name}: {status_text}\n")
            
            # 写入共享缓存，供前端Flask读取
            service_status_cache = temp_cache

        time.sleep(10) # 每10秒巡逻一次，可以调整时间

# --- 5. Flask Web 界面逻辑 (融合了你之前的UI显示) ---
@app.route('/')
def index():
    # 如果后台线程还没来得及第一次检查，显示正在加载
    if not service_status_cache:
        results_html = "<li>⏳ 机器人正在进行首次巡逻，请稍候...</li>"
    else:
        results_list = []
        for name, status in service_status_cache.items():
            results_list.append(f"<li><b>{name}</b>: {status}</li>")
        results_html = "".join(results_list)

    # 保留你原来的 CSS 样式
    html = f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>🚀 JM 的全网监控雷达 v2.1 (飞书告警版)</h1>
            <div style="display: inline-block; text-align: left; border: 1px solid #ccc; padding: 20px; border-radius: 10px;">
                <ul>{results_html}</ul>
            </div>
            <p>最后更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
    </html>
    """
    return html

# --- 6. 主程序入口 ---
if __name__ == '__main__':
    # 🎯 核心改变：在启动 Flask 之前，先启动后台监控线程
    # 设置 daemon=True，主程序退出时线程自动退出
    t = threading.Thread(target=monitoring_worker, daemon=True)
    t.start()

    # 适配 Render 云端动态端口或本地端口适配
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
