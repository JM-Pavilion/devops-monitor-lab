# 1. 使用官方 Python 轻量级镜像作为基础
FROM python:3.9-slim

# 2. 设置容器内部的工作目录
WORKDIR /app

# 3. 先把依赖列表拷进去
COPY requirements.txt .

# 4. 安装依赖 (使用清华源加速，避免网络问题)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 把当前目录下的所有文件（包括 bot.py 和 .env）拷贝到容器里
COPY . .

# 6. 容器启动时执行的命令
CMD ["python", "bot.py"]
