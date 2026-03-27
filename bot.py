import requests
import time
import os
from flask import Flask
import threading

app = Flask(__name__)

# --- 核心修改 1：填入你的飞书机器人地址 ---
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/e99f601a-3a5e-4360-b536-4949eac47a8a"

def send_feishu_alert(service_name, status):
    """当服务出问题时，给飞书发消息"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🚨 告警：服务 [{service_name}] 状态异常！\n当前状态：{status}\n检查时间：{time.ctime()}"
        }
    }
    try:
        requests.post(FEISHU_WEBHOOK, json=payload)
    except Exception as e:
        print(f"发送告警失败: {e}")

# 用于记录上一次的状态，防止重复发消息骚扰你
last_status = {}

def check_health():
    targets = {
        "Baidu": "https://www.baidu.com",
        "GitHub": "https://github.com",
        "LocalHello": "http://hello:80"
    }
    
    while True:
        with open("monitor.log", "a") as f:
            for name, url in targets.items():
                try:
                    r = requests.get(url, timeout=5)
                    status = "Normal" if r.status_code == 200 else f"Error({r.status_code})"
                except:
                    status = "Down"
                
                # --- 核心修改 2：触发告警逻辑 ---
                # 如果状态从 Normal 变成不正常，且不是第一次检查，就发飞书
                if name in last_status and last_status[name] == "Normal" and status != "Normal":
                    send_feishu_alert(name, status)
                
                last_status[name] = status
                f.write(f"{time.ctime()} - {name}: {status}\n")
        time.sleep(10)

# ... 其余 Flask 路由代码保持不变 ...
