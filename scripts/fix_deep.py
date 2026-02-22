#!/usr/bin/env python3
"""
逐行深度修复脚本 - 世界NO.1质量
"""

import ast
import re
from pathlib import Path
from typing import Tuple

def deep_fix_file(filepath: Path) -> Tuple[bool, str]:
    """深度修复单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_count = 0
        fix_log = []

        # 逐行分析和修复
        for i in range(len(lines)):
            line = lines[i]
            original_line = line

            # === 修复1: 装饰器语法 ===
            # @xxx.command(name("yyy") → @xxx.command(name="yyy")
            if re.search(r'@\w+\.command\(name\s*\(\s*["\']', line):
                line = re.sub(r'(@\w+\.command\()name\s*\(\s*(["\'][^"\']*["\'])\s*\)',
                            r'\1name=\2)', line)

            # === 修复2: 缺失的装饰器括号 ===
            if re.search(r'@\w+\.command\(name\s*=\s*["\'][^"\']*["\']\s*$', line):
                if i + 1 < len(lines) and '@click.option' in lines[i + 1]:
                    line = line.rstrip() + ')\n'

            # === 修复3: f-string括号 ===
            # console.print(f("xxx") → console.print(f"xxx")
            line = re.sub(r'console\.print\(f\((["\'][^"\']*["\'])\)', r'console.print(f\1)', line)

            # === 修复4: 修复不匹配的括号 ===
            # 如果一行以console.print(f"或'结尾，添加)
            if re.search(r'console\.print\(f["\'][^"\']*["\'][^)]*\s*$', line):
                line = re.sub(r'(console\.print\(f["\'][^"\']*["\'][^)]*)(\s*)$',
                            r'\1)\2', line)

            # === 修复5: Python 3.8类型注解 ===
            line = re.sub(r':\s*(\w+)\s*\|\s*(\w+)', r': Union[\1, \2]', line)

            if line != original_line:
                fixed_count += 1
                lines[i] = line

        if fixed_count > 0:
            # 验证语法
            content = ''.join(lines)
            try:
                ast.parse(content)

                # 写回
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                return True, f"修复{fixed_count}处"

            except SyntaxError as e:
                return False, f"验证失败: {e.msg} at line {e.lineno}"

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

    print(f"🔥 深度修复 - {len(error_files)}个文件\n")

    fixed = 0
    for filepath in error_files:
        success, log = deep_fix_file(filepath)
        if success:
            fixed += 1
            print(f"✅ {filepath.name}: {log}")
        else:
            print(f"❌ {filepath.name}: {log}")

    print(f"\n📊 修复: {fixed}/{len(error_files)}")

if __name__ == '__main__':
    main()
