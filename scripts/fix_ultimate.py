#!/usr/bin/env python3
"""
终极修复脚本 - 世界NO.1质量
深度修复所有语法问题
"""

import ast
import re
from pathlib import Path
from typing import Tuple

def ultimate_fix(filepath: Path) -> Tuple[bool, str]:
    """终极修复"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fix_log = []

        # === 修复1: 装饰器语法 ===
        # @xxx.command(name("yyy") → @xxx.command(name="yyy")
        pattern1 = r'@(\w+)\.command\(name\s*\(\s*["\']([^"\']+)["\']\s*\)'
        if re.search(pattern1, content):
            content = re.sub(pattern1, r'@\1.command(name="\2")', content)
            if content != original:
                fix_log.append("装饰器语法")

        # === 修复2: 缺失的装饰器括号 ===
        lines = content.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            # @xxx.command(name="yyy" 缺少 )
            if re.search(r'@\w+\.command\(name\s*=\s*["\'][^"\']*["\']\s*$', line):
                if i + 1 < len(lines) and '@click.option' in lines[i + 1]:
                    line = line.rstrip() + ')'
                    fix_log.append("装饰器括号")
            fixed_lines.append(line)
        content = '\n'.join(fixed_lines)

        # === 修复3: f-string括号问题 ===
        # console.print(f("xxx") → console.print(f"xxx")
        content = re.sub(r'console\.print\(f\((["\'][^"\']*["\'])\)', r'console.print(f\1)', content)
        if content != original:
            if 'console.print' not in fix_log:
                fix_log.append("f-string括号")

        # === 修复4: 修复不匹配的括号 ===
        # console.print(f"xxx" → console.print(f"xxx")
        content = re.sub(r'console\.print\(f"([^"]*?)"\s*$', r'console.print(f"\1")', content, flags=re.MULTILINE)
        content = re.sub(r"console\.print\(f'([^']*?)'\s*$", r"console.print(f'\1')", content, flags=re.MULTILINE)

        # === 修复5: Python 3.8兼容性 ===
        # Path | str → Union[Path, str]
        if ' | ' in content:
            # 检查是否需要添加Union导入
            if 'Union' not in content:
                if 'from typing import' in content:
                    # 添加Union到导入
                    content = re.sub(
                        r'(from typing import [^\n]+)',
                        r'\1, Union',
                        content,
                        count=1
                    )
                    fix_log.append("添加Union导入")

            # 修复类型注解
            content = re.sub(r':\s*(\w+)\s*\|\s*(\w+)', r': Union[\1, \2]', content)
            if 'Union[' in content and 'Union导入' not in fix_log:
                fix_log.append("类型注解")

        # list[str] → List[str]
        if 'list[' in content:
            content = re.sub(r'\blist\[', 'List[', content)
            if 'List导入' not in fix_log:
                fix_log.append("list类型")

        # dict[str, ...] → Dict[str, ...]
        if 'dict[' in content:
            content = re.sub(r'\bdict\[', 'Dict[', content)
            if 'Dict导入' not in fix_log:
                fix_log.append("dict类型")

        # === 验证语法 ===
        try:
            ast.parse(content)

            # 写回文件
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, ', '.join(fix_log)
            else:
                return False, "无需修复"

        except SyntaxError as e:
            return False, f"验证失败: {e}"

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

    print(f"🔥 世界NO.1质量修复 - {len(error_files)}个文件\n")

    fixed = 0
    failed = []

    for filepath in error_files:
        success, log = ultimate_fix(filepath)
        if success:
            fixed += 1
            print(f"✅ {filepath.name}: {log}")
        elif log == "无需修复":
            print(f"⏭️  {filepath.name}: {log}")
        else:
            failed.append((filepath.name, log))
            print(f"❌ {filepath.name}: {log}")

    print(f"\n📊 修复统计:")
    print(f"  ✅ 成功: {fixed}")
    print(f"  ❌ 失败: {len(failed)}")
    print(f"  📈 成功率: {fixed*100//len(error_files)}%")

    if failed:
        print(f"\n⚠️ 需要手动修复:")
        for name, reason in failed:
            print(f"  - {name}: {reason}")

if __name__ == '__main__':
    main()
