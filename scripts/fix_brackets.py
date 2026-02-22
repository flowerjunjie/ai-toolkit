#!/usr/bin/env python3
"""
修复缺失的括号和引号
"""

from pathlib import Path
import ast

def fix_missing_brackets(filepath: Path) -> bool:
    """修复缺失的括号"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 修复: console.print(f"...\n" → console.print(f"...\n")
        content = content.replace('console.print(f"\\n', 'console.print(f"\\n')
        content = content.replace('console.print(f"\\n', 'console.print(f"\\n')

        # 修复所有未闭合的console.print
        import re
        # 查找 console.print(f"..." 后面没有 ) 的情况
        pattern = r'console\.print\(f"([^"]*\\n[^"]*)"(?!\))'
        content = re.sub(pattern, r'console.print(f"\1)"', content)

        # 修复其他未闭合的括号
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # 如果一行有 console.print(f"... 但没有闭合括号
            if 'console.print(f"' in line and line.count('(') > line.count(')'):
                # 检查是否以引号结尾
                if line.rstrip().endswith('"') or line.rstrip().endswith("'"):
                    line = line.rstrip() + ')'
            fixed_lines.append(line)

        content = '\n'.join(fixed_lines)

        if content != original:
            # 验证语法
            try:
                ast.parse(content)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except SyntaxError:
                return False

        return False

    except Exception as e:
        return False

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    fixed = 0

    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue

        if fix_missing_brackets(py_file):
            fixed += 1
            print(f"✅ {py_file.name}: 修复括号")

    print(f"\n✅ 修复了 {fixed} 个文件")

if __name__ == '__main__':
    main()
