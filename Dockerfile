FROM python:3.11-slim

LABEL maintainer="David"
LABEL description="AI Toolkit - 本地AI工具箱"

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# 复制项目文件
COPY . .

# 安装项目
RUN pip install --no-cache-dir -e ".[rag]"

# 暴露端口（如果需要 Web UI）
EXPOSE 8000

# 默认命令
CMD ["ai-toolkit", "--help"]
