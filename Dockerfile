#1.使用轻量级的Python基础环境
FROM python:3.9-slim

#2.设置容器内部的工作目录
WORKDIR /app

#3.将当前目录下的所有文件复制到容器的工作目录中
COPY . .

#4.暴露我们在代码里的定义的80端口
EXPOSE 80

#5.启动机器人的命令
CMD [ "python", "bot.py" ]