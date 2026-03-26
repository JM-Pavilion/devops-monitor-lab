import requests
import time
from flask import Flask

app = Flask(__name__)

# 🎯 监控名单：一个是内部邻居，一个是外部大厂
TARGETS = {
    "Internal-Hello-Service": "http://hello",
    "External-Baidu": "https://www.baidu.com",
    "External-GitHub": "https://github.com"
}

def check_services():
    results = []
    for name, url in TARGETS.items():
        try:
            resp = requests.get(url, timeout=3)
            status = "✅ 运行正常" if resp.status_code == 200 else f"⚠️ 状态码: {resp.status_code}"
        except:
            status = "❌ 发现故障"
        results.append(f"<li><b>{name}</b>: {status}</li>")
    return "".join(results)

@app.route('/')
def index():
    html = f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>🚀 JM 的全网监控雷达 v2.0</h1>
            <div style="display: inline-block; text-align: left; border: 1px solid #ccc; padding: 20px; border-radius: 10px;">
                <ul>{check_services()}</ul>
            </div>
            <p>最后更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
