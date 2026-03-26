import http.server
import socketserver
import threading
import urllib.request
impor time
from datetime import datetime

# --- 配置区 ---
MONITOR_URL = "http://hello"
PORT = 80  # 容器内部开启 80 端口
status_report = "🚀 哨兵启动中..."

# --- 1. 网页服务逻辑 ---
class StatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        # 网页模板：每 5 秒自动刷新一次
        html = f"""
        <html>
        <head><meta http-equiv="refresh" content="5"><title>DevOps Monitor</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f4f4f9;">
            <h1>🛠️ 服务实时监控大屏</h1>
            <div style="font-size: 24px; padding: 20px; border-radius: 10px; display: inline-block; 
                 background: {'#d4edda' if 'OK' in status_report else '#f8d7da'}; 
                 color: {'#155724' if 'OK' in status_report else '#721c24'};">
                {status_report}
            </div>
            <p style="color: #666;">最后更新时间: {datetime.now().strftime('%H:%M:%S')}</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

def run_web_server():
    with socketserver.TCPServer(("", PORT), StatusHandler) as httpd:
        print(f"📡 网页大屏已在容器 {PORT} 端口上线")
        httpd.serve_forever()

# --- 2. 监控逻辑 ---
def monitor():
    global status_report
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        try:
            res = urllib.request.urlopen(MONITOR_URL, timeout=2)
            status_report = f"✅ [{now}] 服务在线 - 状态码: {res.getcode()}"
        except Exception as e:
            status_report = f"❌ [{now}] 发现故障 - 原因: {e}"
        time.sleep(5)

# --- 启动：多线程并行 ---
threading.Thread(target=run_web_server, daemon=True).start()
monitor()
