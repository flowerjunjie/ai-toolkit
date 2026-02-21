#!/bin/bash
# 开发环境设置脚本

set -e

echo "🔧 设置 AI Toolkit 开发环境..."

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install -e ".[dev]"

# 创建示例配置文件
echo "📝 创建示例配置..."
python3 -c "from ai_toolkit.core.api_manager import create_sample_config; create_sample_config()"

# 运行测试
echo "🧪 运行测试..."
pytest tests/ -v

echo "✅ 开发环境设置完成！"
