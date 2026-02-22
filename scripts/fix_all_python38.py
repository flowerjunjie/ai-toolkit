#!/usr/bin/env python3
"""
批量修复Python 3.8兼容性问题
"""

import re
import ast
from pathlib import Path
from typing import List, Tuple

def fix_python38_compatibility(content: str) -> Tuple[str, int]:
    """
    修复Python 3.8兼容性问题
    返回: (修复后的内容, 修复数量)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []

    # 添加需要的导入
    imports_needed = []
    has_union_import = False
    has_list_import = False
    has_dict_import = False

    for line in lines:
        # 检查导入
        if 'from typing import' in line:
            if 'Union' in line:
                has_union_import = True
            if 'List' in line:
                has_list_import = True
            if 'Dict' in line:
                has_dict_import = True
            fixed_lines.append(line)
            continue

        # 修复类型注解
        original_line = line

        # 修复: Path | str → Union[Path, str]
        if ' | ' in line and ':' in line:
            # 检查是否是类型注解
            if ')' in line or '=' in line or ':' in line:
                # 替换类型联合
                line = re.sub(r'(\w+)\s*\|\s*(\w+)', r'Union[\1, \2]', line)

                if 'Union' in line and not has_union_import:
                    imports_needed.append('Union')
                    has_union_import = True
                fixes += 1

        # 修复: list[str] → List[str]
        line = re.sub(r'\blist\[', r'List[', line)
        if 'List[' in line and not has_list_import and 'List' not in imports_needed:
            imports_needed.append('List')
            has_list_import = True

        # 修复: dict[str, ...] → Dict[str, ...]
        line = re.sub(r'\bdict\[', r'Dict[', line)
        if 'Dict[' in line and not has_dict_import and 'Dict' not in imports_needed:
            imports_needed.append('Dict')
            has_dict_import = True

        # 修复装饰器语法: @command(name("xxx") → @command(name="xxx")
        line = re.sub(r'@(\w+)\(\s*name\s*\(\s*["\']', r'@\1(name="', line)
        if ')' in line and line.count('(') > line.count(')'):
            # 添加缺失的右括号
            line += ')'

        # 修复: console.print(f("xxx") → console.print(f"xxx")
        line = re.sub(r'console\.print\(f\(("([^"]|\\")*")\)', r'console.print(f"\1)', line)

        # 修复: console.print(f("xxx') → console.print(f"xxx')
        line = re.sub(r'console\.print\(f\(("([^\'|\\)|\\\']*)"\)', r'console.print(f"\1)', line)

        if line != original_line:
            fixes += 1

        fixed_lines.append(line)

    # 在开头添加需要的导入
    if imports_needed:
        result_lines = []
        imports_to_add = set(imports_needed)

        # 找到from typing import行并添加
        for i, line in enumerate(fixed_lines):
            if 'from typing import' in line:
                # 添加缺失的导入
                existing_imports = line.split('from typing import')[1].split(')')[0].strip()
                existing_list = [x.strip() for x in existing_imports.split(',') if x.strip()]

                for imp in imports_to_add:
                    if imp not in existing_list:
                        existing_list.append(imp)

                new_import = f"from typing import {', '.join(existing_list)}"
                result_lines.append(new_import)
                imports_to_add.clear()
            else:
                result_lines.append(line)

        # 如果没有typing导入，添加一个
        if imports_to_add:
            result_lines.insert(0, f"from typing import {', '.join(imports_to_add)}")

        fixed_lines = result_lines

    return '\n'.join(fixed_lines), fixes

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    print(f"🔍 扫描 {len(py_files)} 个文件...")

    fixed_count = 0
    error_count = 0

    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue

        # 读取文件
        with open(py_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # 修复
        fixed_content, fixes = fix_python38_compatibility(original_content)

        if fixes > 0:
            # 验证语法
            try:
                ast.parse(fixed_content)

                # 写回文件
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

                print(f"✅ {py_file.name}: 修复 {fixes} 处")
                fixed_count += 1

            except SyntaxError as e:
                print(f"❌ {py_file.name}: 修复失败 - {e}")
                error_count += 1

    print(f"\n📊 修复统计:")
    print(f"  修复成功: {fixed_count}")
    print(f"  修复失败: {error_count}")
    print(f"  无需修复: {len(py_files) - fixed_count - error_count}")

if __name__ == '__main__':
    main()
