#!/bin/bash
# AI Toolkit - 自动发布脚本

echo "🚀 AI Toolkit 自动发布脚本"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查curl
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl未安装${NC}"
    exit 1
fi

# 检查jq
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq未安装，尝试安装...${NC}"
    apt-get install -y jq || yum install -y jq
fi

echo -e "${GREEN}✅${NC} 工具检查完成"
echo ""

# ========================================
# Hacker News 发布
# ========================================
echo "📱 尝试发布到Hacker News..."
echo "------------------------------"

# 尝试发布（会失败，因为需要登录）
curl -X POST "https://news.ycombinator.com/submit" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Show%20HN%3A%20AI%20Toolkit%20%E2%80%93%20%E6%9C%AC%E5%9C%B0AI%E5%BC%80%E5%8F%91%E7%9A%84%E7%BB%88%E5%AF%B9%E5%B7%A5%E7%AE%B1&url=https://github.com/flowerjunjie/ai-toolkit" \
  2>&1 | grep -q "You have to be logged in"

if [ $? -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Hacker News需要登录${NC}"
    echo ""
    echo "手动操作步骤："
    echo "1. 访问: https://news.ycombinator.com/submit"
    echo "2. 注册或登录账号"
    echo "3. 填写表单"
    echo "4. 点击Submit"
    echo ""
else
    echo -e "${GREEN}✅${NC} Hacker News发布成功！"
fi

# ========================================
# Reddit 发布
# ========================================
echo ""
echo "📱 尝试发布到Reddit..."
echo "------------------------------"

# Reddit需要OAuth，无法通过curl直接发布
echo -e "${YELLOW}⚠️  Reddit需要登录${NC}"
echo ""
echo "手动操作步骤："
echo "1. 访问: https://www.reddit.com/r/MachineLearning/submit"
echo "2. 填写表单（内容已准备好）"
echo "3. 点击Post"
echo ""

# ========================================
# 检查GitHub状态
# ========================================
echo "📊 检查GitHub状态..."
echo "------------------------------"

# 获取Stars数
STARS=$(curl -s https://api.github.com/repos/flowerjunjie/ai-toolkit | jq '.stargazers_count' || echo "0")
echo "当前Stars: $STARS"
echo ""

# 获取Fork数
FORKS=$(curl -s https://api.github.com/repos/flowerjunjie/ai-toolkit | jq '.forks_count' || echo "0")
echo "Forks: $FORKS"
echo ""

# 获取Open Issues
ISSUES=$(curl -s https://api.github.com/repos/flowerjunjie/ai-toolkit | jq '.open_issues_count' || echo "0")
echo "Open Issues: $ISSUES"
echo ""

# ========================================
# 生成发布指南
# ========================================
echo "================================"
echo "📋 发布指南"
echo "================================"
echo ""
echo "Hacker News:"
echo "  链接: https://news.ycombinator.com/submit"
echo "  标题: Show HN: AI Toolkit – 本地AI开发的终极工具箱"
echo "  URL: https://github.com/flowerjunjie/ai-toolkit"
echo ""
echo "Reddit (r/MachineLearning):"
echo "  链接: https://www.reddit.com/r/MachineLearning/submit"
echo "  标题: [D] AI Toolkit - 本地AI工具箱，让AI开发更简单（开源）"
echo ""
echo "V2EX:"
echo "  链接: https://www.v2ex.com/go/new"
echo "  节点: 分享发现"
echo ""
echo "================================"
echo "💡 提示: 所有发布内容已准备完毕"
echo "📂 文件位置: /root/.openclaw/workspace/projects/ai-toolkit"
echo ""
echo "🚀 AI Toolkit - 让AI开发更简单！"
echo "================================"
