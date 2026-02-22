#!/usr/bin/env python3
"""
第1轮修复 - 彻底修复所有语法错误
"""

import ast
import re
from pathlib import Path
from typing import List, Tuple

def round1_fix(filepath: Path) -> Tuple[bool, str]:
    """第1轮修复"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fixes = []

        # === 修复1: 所有装饰器语法 ===
        # 匹配 @xxx.command(name("yyy") 和 @xxx.command(name="yyy"
        patterns = [
            (r'@(\w+)\.command\(name\s*\(\s*["\']([^"\']+)["\']\s*\)', r'@\1.command(name="\2")'),
            (r'@(\w+)\.command\(name\s*=\s*["\']([^"\']+)["\']\s*$', r'@\1.command(name="\2")'),
        ]

        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if new_content != content:
                fixes.append("装饰器语法")
                content = new_content

        # === 修复2: 添加缺失的装饰器括号 ===
        lines = content.split('\n')
        for i in range(len(lines)):
            # 如果行以 @xxx.command(name="yyy" 结尾（没有右括号）
            if re.search(r'@\w+\.command\(name\s*=\s*["\'][^"\']*["\']\s*$', lines[i]):
                # 检查下一行是否是 @click.option
                if i + 1 < len(lines) and '@click.option' in lines[i + 1]:
                    lines[i] = lines[i].rstrip() + ')'
                    if "括号" not in fixes:
                        fixes.append("装饰器括号")

        content = '\n'.join(lines)

        # === 修复3: f-string问题 ===
        # console.print(f("xxx") → console.print(f"xxx")
        content = re.sub(r'console\.print\(f\((["\'][^"\']*["\'])\)', r'console.print(f\1)', content)
        if content != original and 'f-string' not in fixes:
            fixes.append("f-string")

        # === 修复4: Python 3.8兼容性 ===
        # list[str] → List[str]
        if 'list[' in content:
            content = re.sub(r'\blist\[', 'List[', content)
            if 'list类型' not in fixes:
                fixes.append('list类型')

        # dict[str, ...] → Dict[str, ...]
        if 'dict[' in content:
            content = re.sub(r'\bdict\[', 'Dict[', content)
            if 'dict类型' not in fixes:
                fixes.append('dict类型')

        # Path | str → Union[Path, str]
        if ' | ' in content and 'Union[' not in content:
            content = re.sub(r':\s*(\w+)\s*\|\s*(\w+)', r': Union[\1, \2]', content)
            if 'Union类型' not in fixes:
                fixes.append('Union类型')

        # === 验证语法 ===
        if content != original:
            try:
                ast.parse(content)

                # 写回
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                return True, ', '.join(fixes)

            except SyntaxError as e:
                return False, f"验证失败: {e.msg} at {e.lineno}"

        return False, "无需修复"

    except Exception as e:
        return False, f"错误: {e}"

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    # 找出所有错误文件
    error_files = []
    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
        except SyntaxError:
            error_files.append(py_file)

    print(f"🔧 第1轮修复 - {len(error_files)}个文件\n")

    fixed = 0
    failed = []

    for filepath in error_files:
        success, log = round1_fix(filepath)
        if success:
            fixed += 1
            print(f"✅ {filepath.name}: {log}")
        elif log == "无需修复":
            print(f"⏭️  {filepath.name}: {log}")
        else:
            failed.append((filepath.name, log))
            print(f"❌ {filepath.name}: {log}")

    print(f"\n📊 第1轮结果:")
    print(f"  ✅ 修复成功: {fixed}")
    print(f"  ❌ 修复失败: {len(failed)}")
    print(f"  📈 成功率: {fixed*100//len(error_files)}%")

    if failed:
        print(f"\n⚠️ 需要手动修复:")
        for name, reason in failed:
            print(f"  - {name}: {reason}")

if __name__ == '__main__':
    main()
