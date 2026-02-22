#!/usr/bin/env python3
"""
智能批量修复脚本 - 直接定位并修复
"""

import ast
import re
from pathlib import Path

def smart_fix(filepath: Path) -> bool:
    """智能修复"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fixes = 0

        # 修复1: 缺失的装饰器括号
        lines = content.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            # @xxx.command(name="yyy" 缺少 )
            if re.search(r'@\w+\.command\(name\s*=\s*["\'][^"\']*["\']\s*$', line):
                if i + 1 < len(lines) and '@click.option' in lines[i + 1]:
                    lines[i] = line.rstrip() + ')'
                    fixes += 1

        content = '\n'.join(lines)

        # 修复2: console.print(f"...\n" 缺失 )
        pattern = r'console\.print\(f"([^"]*\\n[^"]*)"(?!\))'
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                old = f'console.print(f"{match}"'
                new = f'console.print(f"{match}")'
                content = content.replace(old, new)
                fixes += 1

        # 修复3: console.print(f'...\n') 缺失 )
        pattern2 = r"console\.print\(f'([^']*\\n[^']*)'(?!\))"
        matches2 = re.findall(pattern2, content)
        if matches2:
            for match in matches2:
                old = f"console.print(f'{match}'"
                new = f"console.print(f'{match}')"
                content = content.replace(old, new)
                fixes += 1

        if fixes > 0:
            # 验证
            try:
                ast.parse(content)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except SyntaxError as e:
                print(f"  ⚠️ 验证失败: {e}")
                return False

        return False

    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    # 找出有错误的文件
    error_files = []
    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
        except SyntaxError:
            error_files.append(py_file)

    print(f"🔍 修复 {len(error_files)} 个错误文件")

    fixed = 0
    for filepath in error_files:
        if smart_fix(filepath):
            fixed += 1
            print(f"✅ {filepath.name}")
        else:
            print(f"❌ {filepath.name}")

    print(f"\n✅ 修复了 {fixed}/{len(error_files)} 个文件")

    # 验证
    remaining = 0
    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
        except SyntaxError:
            remaining += 1

    print(f"⏳ 剩余错误: {remaining}")

if __name__ == '__main__':
    main()
