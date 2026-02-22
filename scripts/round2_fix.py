#!/usr/bin/env python3
"""
第2轮修复 - 修复缺失的括号
"""

import ast
import re
from pathlib import Path

def round2_fix(filepath: Path):
    """第2轮修复"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed = False

        for i in range(len(lines)):
            line = lines[i]

            # 修复: console.print(f"...\n" → console.print(f"...\n")
            # 如果行以 console.print(f" 或 ' 结尾但后面没有 )
            if re.search(r'console\.print\(f["\'][^"\']*["\'][^)]*\s*$', line):
                # 添加缺失的 )
                lines[i] = re.sub(
                    r'(console\.print\(f["\'][^"\']*["\'][^)]*)(\s*)$',
                    r'\1)\2',
                    line
                )
                fixed = True

        if fixed:
            content = ''.join(lines)

            # 验证
            try:
                ast.parse(content)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                return True, "修复括号"
            except SyntaxError as e:
                return False, f"验证失败: {e}"

        return False, "无需修复"

    except Exception as e:
        return False, f"错误: {e}"

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    # 找出错误文件
    error_files = []
    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
        except SyntaxError:
            error_files.append(py_file)

    print(f"🔧 第2轮修复 - {len(error_files)}个文件\n")

    fixed = 0
    for filepath in error_files:
        success, log = round2_fix(filepath)
        if success:
            fixed += 1
            print(f"✅ {filepath.name}: {log}")
        else:
            print(f"❌ {filepath.name}: {log}")

    print(f"\n📊 第2轮结果: 修复了 {fixed} 个文件")

if __name__ == '__main__':
    main()
