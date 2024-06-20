# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄下的所有文件到工作目錄
COPY . .

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用程式運行的端口
EXPOSE 5008

# 定義容器啟動時運行的命令
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5004 5005 5008 5009

CMD ["sh", "-c", "python news_service.py & python stock_service.py & python sentiment_analysis_service.py & python app.py"]