#1.使用轻量级的Python基础环境
FROM python:3.9-slim

#2.设置容器内部的工作目录
WORKDIR /app

RUN pip install requests flask

COPY . .

#4.暴露我们在代码里的定义的80端口
EXPOSE 80

#5.启动机器人的命令
CMD [ "python", "bot.py" ]