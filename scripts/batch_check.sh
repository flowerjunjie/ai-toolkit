#!/bin/bash
# 批量检查所有Python文件语法

echo "🔍 批量语法检查..."
echo ""

ERRORS=0
CHECKED=0

for file in src/ai_toolkit/commands/*.py; do
    CHECKED=$((CHECKED + 1))
    filename=$(basename "$file")
    
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "✅ $filename"
    else
        echo "❌ $filename"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "📊 检查结果:"
echo "  检查: $CHECKED 个文件"
echo "  错误: $ERRORS 个文件"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ 所有文件语法正确！"
    exit 0
else
    echo "❌ 还有 $ERRORS 个文件需要修复"
    exit 1
fi
