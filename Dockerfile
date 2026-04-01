FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# 移除了清华源，因为 Render 在海外，用清华源反而会拉取失败
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
