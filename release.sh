#!/bin/bash
# AI Toolkit - 社区发布自动化脚本

set -e

PROJECT_DIR="/root/.openclaw/workspace/projects/ai-toolkit"
cd "$PROJECT_DIR"

echo "🚀 AI Toolkit 社区发布脚本"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 步骤1: 检查Git状态
echo "📋 步骤1: 检查Git状态"
echo "------------------------------"
git status
echo ""

# 步骤2: 检查最新提交
echo "📋 步骤2: 检查最新提交"
echo "------------------------------"
git log -1 --oneline
echo ""

# 步骤3: 检查GitHub Stars
echo "📋 步骤3: 检查GitHub Stars"
echo "------------------------------"
STARS=$(curl -s https://api.github.com/repos/flowerjunjie/ai-toolkit | grep -o '"stargazers_count": [0-9]*' | grep -o '[0-9]*' || echo "0")
echo "当前Stars: $STARS"
echo ""

# 步骤4: 检查文档
echo "📋 步骤4: 检查文档"
echo "------------------------------"
echo "核心文档:"
ls -1 *.md 2>/dev/null | grep -E "(README|QUICKSTART|FAQ|CHANGELOG)" || echo "未找到"
echo ""
echo "推广文档:"
ls -1 PROMO*.md 2>/dev/null | wc -l
echo "个推广文档"
echo ""

# 步骤5: 统计代码
echo "📋 步骤5: 统计代码"
echo "------------------------------"
echo "功能模块:"
find src/ai_toolkit/commands -name "*.py" 2>/dev/null | wc -l
echo "个命令文件"
echo ""
echo "代码行数:"
find src -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 || echo "0"
echo ""

# 步骤6: 测试安装
echo "📋 步骤6: 测试安装"
echo "------------------------------"
echo "测试版本:"
ai-toolkit --version 2>/dev/null || echo "未安装"
echo ""

# 步骤7: 检查远程仓库
echo "📋 步骤7: 检查远程仓库"
echo "------------------------------"
git remote -v
echo ""

# 步骤8: 发布就绪检查
echo "📋 步骤8: 发布就绪检查"
echo "------------------------------"
READY=true

# 检查README
if [ -f "README.md" ]; then
    echo -e "${GREEN}✓${NC} README.md 存在"
else
    echo -e "${RED}✗${NC} README.md 缺失"
    READY=false
fi

# 检查LICENSE
if [ -f "LICENSE" ]; then
    echo -e "${GREEN}✓${NC} LICENSE 存在"
else
    echo -e "${YELLOW}⚠${NC} LICENSE 缺失（建议添加）"
fi

# 检查推广内容
if [ -f "PROMO_REDDIT.md" ] && [ -f "PROMO_HACKERNEWS.md" ]; then
    echo -e "${GREEN}✓${NC} 推广内容准备完成"
else
    echo -e "${RED}✗${NC} 推广内容缺失"
    READY=false
fi

# 检查快速开始
if [ -f "QUICKSTART_CN.md" ]; then
    echo -e "${GREEN}✓${NC} 快速开始指南存在"
else
    echo -e "${YELLOW}⚠${NC} 快速开始指南缺失（建议添加）"
fi

# 检查FAQ
if [ -f "FAQ.md" ]; then
    echo -e "${GREEN}✓${NC} FAQ存在"
else
    echo -e "${YELLOW}⚠${NC} FAQ缺失（建议添加）"
fi

echo ""

# 步骤9: 生成发布链接
echo "📋 步骤9: 发布链接"
echo "------------------------------"
echo "Hacker News:"
echo "https://news.ycombinator.com/submit"
echo ""
echo "Reddit (r/MachineLearning):"
echo "https://www.reddit.com/r/MachineLearning/submit"
echo ""
echo "V2EX:"
echo "https://www.v2ex.com/go/new"
echo ""

# 步骤10: 监控命令
echo "📋 步骤10: 监控命令"
echo "------------------------------"
echo "查看Stars:"
echo "  curl -s https://api.github.com/repos/flowerjunjie/ai-toolkit | jq '.stargazers_count'"
echo ""
echo "查看Issues:"
echo "  gh repo view flowerjunjie/ai-toolkit --json issues,openIssuesCount"
echo ""
echo "查看Traffic（需要GitHub CLI）:"
echo "  gh repo view flowerjunjie/ai-toolkit --traffic"
echo ""

# 最终结论
echo "================================"
if [ "$READY" = true ]; then
    echo -e "${GREEN}✅ 发布准备完成！${NC}"
    echo ""
    echo "🎯 下一步行动："
    echo "1. 访问 Hacker News: https://news.ycombinator.com/submit"
    echo "2. 访问 Reddit: https://www.reddit.com/r/MachineLearning/submit"
    echo "3. 访问 V2EX: https://www.v2ex.com/go/new"
    echo ""
    echo "📊 当前Stars: $STARS"
    echo "🚀 目标（第1周）: +200 Stars"
    echo "🎯 目标（第1月）: +1000 Stars"
else
    echo -e "${RED}❌ 发布准备未完成！${NC}"
    echo ""
    echo "请完成以上缺失的项目后再发布。"
fi
echo ""
echo "================================"
echo "🚀 AI Toolkit - 让AI开发更简单！"
echo "================================"
