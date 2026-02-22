#!/usr/bin/env python3
"""
精准修复装饰器语法错误
"""

from pathlib import Path

def fix_decorator_syntax(filepath: Path) -> bool:
    """修复装饰器语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        fixed = False

        for i, line in enumerate(lines):
            # 检查是否是装饰器行
            if line.strip().startswith('@') and '(' in line and ')' not in line:
                # 这一行装饰器没有闭合的括号
                # 检查下一行是否是@click.option
                if i + 1 < len(lines) and '@click.option' in lines[i + 1]:
                    # 修复: 闭合装饰器的括号
                    line = line.rstrip() + ')\n'
                    fixed = True

            fixed_lines.append(line)

        if fixed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            return True

        return False

    except Exception as e:
        print(f"❌ {filepath.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted(commands_dir.glob('*.py'))

    fixed = 0

    for py_file in py_files:
        if py_file.name.startswith('_'):
            continue

        if fix_decorator_syntax(py_file):
            fixed += 1
            print(f"✅ {py_file.name}: 修复装饰器")

    print(f"\n✅ 修复了 {fixed} 个文件的装饰器语法")

if __name__ == '__main__':
    main()
