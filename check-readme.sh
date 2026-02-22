#!/bin/bash
# README更新检查脚本

echo "📋 检查README更新状态"
echo "========================"
echo ""

# 获取最后一次提交时间
LAST_COMMIT=$(git log -1 --format=%ct README.md 2>/dev/null || echo "0")
CURRENT_TIME=$(date +%s)
TIME_DIFF=$((CURRENT_TIME - LAST_COMMIT))
TIME_DIFF_HOURS=$((TIME_DIFF / 3600))

echo "README最后更新: $TIME_DIFF_HOURS 小时前"
echo ""

if [ $TIME_DIFF_HOURS -gt 24 ]; then
    echo "⚠️  警告: README超过24小时未更新！"
    echo ""
    echo "建议更新内容："
    echo "  - 添加最新功能"
    echo "  - 更新项目数据"
    echo "  - 添加用户案例"
    echo "  - 更新Stars数"
    echo ""
    echo "更新命令:"
    echo "  1. 编辑README.md"
    echo "  2. git add README.md"
    echo "  3. git commit -m 'docs: 更新README'"
    echo "  4. git push origin main"
else
    echo "✅ README状态良好"
fi

echo ""
echo "========================"
