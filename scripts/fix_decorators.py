#!/usr/bin/env python3
"""
修复所有装饰器语法错误
"""

import re
from pathlib import Path

def fix_all_decorator_issues(file_path):
    """修复装饰器问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        modified = False
        
        # 修复1: 未闭合的装饰器
        # @xxx.command(name="yyy" -> @xxx.command(name="yyy")
        content = re.sub(
            r'@(\w+\.\w+)\(name\("([^"]+)"\)\s*\n',
            r'@\1.command(name="\2")\n',
            content
        )
        if content != original:
            modified = True
            original = content
        
        # 修复2: @xxx.group(name="yyy" -> @xxx.group(name="yyy")
        content = re.sub(
            r'@(\w+\.\w+)\(name\("([^"]+)"\)\s*\n',
            r'@\1.group(name="\2")\n',
            content
        )
        if content != original:
            modified = True
            original = content
        
        # 修复3: console.print(f("xxx") -> console.print(f"xxx")
        content = re.sub(
            r'console\.print\(f\(',
            'console.print(f"',
            content
        )
        if content != original:
            modified = True
            original = content
        
        # 修复4: f("xxx") -> f"xxx"
        content = re.sub(
            r'=\s*f\(',
            '= f"',
            content
        )
        if content != original:
            modified = True
            original = content
        
        # 修复5: help("xxx") -> help="xxx"
        content = re.sub(
            r'help\("([^"]+)"\)(?=[,)])',
            r'help="\1"',
            content
        )
        if content != original:
            modified = True
            original = content
        
        # 修复6: default("xxx") -> default="xxx"
        content = re.sub(
            r'default\("([^"]+)"\)(?=[,)])',
            r'default="\1"',
            content
        )
        if content != original:
            modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 修复所有装饰器问题...")
    print()
    
    fixed_count = 0
    total = 0
    
    for py_file in sorted(commands_dir.glob("*.py")):
        total += 1
        if fix_all_decorator_issues(py_file):
            print(f"✅ {py_file.name}")
            fixed_count += 1
    
    print()
    print(f"📊 修复: {fixed_count}/{total} 个文件")

if __name__ == "__main__":
    main()
