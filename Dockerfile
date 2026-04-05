# 第一阶段：编译阶段 (Builder)
FROM python:3.9-slim AS builder
WORKDIR /app

# 修正：针对新版 Debian (Bookworm) 的换源路径
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ... 第二阶段：运行阶段 (Final) ...
FROM python:3.9-slim
WORKDIR /app

# 同样在这里也换一下源，确保以后安装 curl 没问题
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 只有换源成功了，这一步才不会报 exit code 100
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# 只从第一阶段把装好的库拷过来
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "bot.py"]


# 每 30 秒检查一次，如果连续 3 次失败，就标记为 unhealthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1
