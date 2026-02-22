#!/usr/bin/env python3
"""
自动修复Python文件中的装饰器语法错误
"""

import re
from pathlib import Path

def fix_decorator_syntax(file_path):
    """修复装饰器语法"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复 @click.command(name="xxx") -> @click.command(name="xxx")
    content = re.sub(r'@(\w+)\.command\(name\("([^"]+)"\)', 
                    r'@\1.command(name="\2"', content)
    
    # 修复 @click.option("--xxx", "-x", default("yyy", help("zzz")) 
    # -> @click.option("--xxx", "-x", default="yyy", help="zzz"
    content = re.sub(r'(@click\.option\([^)]+, )default\("([^"]+)"\)(, help\("([^"]+)"\))',
                    r'\1default="\2"\3', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    fixed_count = 0
    for py_file in commands_dir.glob("*.py"):
        if fix_decorator_syntax(py_file):
            print(f"✅ 修复: {py_file.name}")
            fixed_count += 1
    
    print(f"\n📊 修复完成: {fixed_count} 个文件")

if __name__ == "__main__":
    main()
