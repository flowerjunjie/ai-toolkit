#!/bin/bash
# 语法检查脚本

echo "🔍 检查Python文件语法..."

ERRORS=0
FILES=src/ai_toolkit/commands/*.py

for file in $FILES; do
    echo "检查: $file"
    python3 -m py_compile "$file" 2>&1
    if [ $? -ne 0 ]; then
        echo "❌ 语法错误: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ 语法正确: $file"
    fi
done

echo ""
echo "📊 检查完成:"
echo "  总文件: $(ls src/ai_toolkit/commands/*.py | wc -l)"
echo "  错误: $ERRORS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ 所有文件语法正确！"
    exit 0
else
    echo "❌ 发现 $ERRORS 个文件有语法错误"
    exit 1
fi
