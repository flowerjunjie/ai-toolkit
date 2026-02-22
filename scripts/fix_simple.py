#!/usr/bin/env python3
"""
批量修复Python 3.8兼容性问题 - 简化版
"""

import re
import ast
from pathlib import Path

def fix_file(filepath: Path) -> bool:
    """修复单个文件"""
    try:
        # 读取文件
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 修复1: Path | str → Union[Path, str]
        content = re.sub(r':\s*(\w+)\s*\|\s*(\w+)', r': Union[\1, \2]', content)

        # 修复2: list[str] → List[str]
        content = re.sub(r'\blist\[', 'List[', content)

        # 修复3: dict[str, ...] → Dict[str, ...]
        content = re.sub(r'\bdict\[', 'Dict[', content)

        # 添加Union导入
        if 'Union[' in content and 'from typing import' in content:
            # 检查是否已有Union
            if 'from typing import' in content and 'Union' not in content.split('from typing import')[1].split('\n')[0]:
                # 在typing导入中添加Union
                content = re.sub(
                    r'(from typing import [^\n]+)',
                    r'\1, Union',
                    content,
                    count=1
                )

        # 验证语法
        ast.parse(content)

        # 写回
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"❌ {filepath.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    print(f"🔍 扫描 {len(py_files)} 个文件...")

    # 先找出所有有语法错误的文件
    error_files = []
    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError:
            error_files.append(py_file)

    print(f"❌ 发现 {len(error_files)} 个语法错误文件")

    if not error_files:
        print("✅ 所有文件语法正确！")
        return

    # 修复
    fixed = 0
    for filepath in error_files[:10]:  # 先修复10个
        print(f"  修复 {filepath.name}...")
        if fix_file(filepath):
            fixed += 1
            print(f"    ✅ {filepath.name} 修复成功")
        else:
            print(f"    ❌ {filepath.name} 修复失败")

    print(f"\n✅ 修复了 {fixed}/{len(error_files[:10])} 个文件")
    print(f"⏳ 剩余 {len(error_files) - 10} 个文件")

if __name__ == '__main__':
    main()
