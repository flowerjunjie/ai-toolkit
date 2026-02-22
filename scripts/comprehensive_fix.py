#!/usr/bin/env python3
"""
全面修复Python语法错误
"""

import re
from pathlib import Path

def fix_syntax_errors(content):
    """修复语法错误"""
    lines = content.split('\n')
    fixed_lines = []
    modified = False
    
    for line in lines:
        original = line
        
        # 修复1: console.print(f("xxx") -> console.print(f"xxx")
        line = re.sub(r'console\.print\(f\("([^"]*)"', r'console.print(f"\1"', line)
        line = re.sub(r'console\.print\(f"([^"]+)"\)', r'console.print(f"\1")', line)
        
        # 修复2: f("xxx") -> f"xxx"
        line = re.sub(r'=\s*f\("([^"]+)""\)', r'= f"\1""', line)
        
        # 修复3: help("xxx") -> help="xxx"
        line = re.sub(r'help\("([^"]+)"\)(?=[,)])', r'help="\1"', line)
        
        # 修复4: default("xxx") -> default="xxx"
        line = re.sub(r'default\("([^"]+)"\)(?=[,)])', r'default="\1"', line)
        
        # 修复5: choice("xxx", "yyy") -> choice=["xxx", "yyy"]
        line = re.sub(r'choice\("([^"]+)",\s*"([^"]+)"\)', r'choice=["\1", "\2"]', line)
        
        # 修复6: console print ( -> console.print(
        line = line.replace('console print(', 'console.print(')
        
        # 修复7: 中文引号问题
        line = line.replace('"', '"').replace('"', '"')
        
        # 修复8: 三引号问题
        line = line.replace('"""', '"""')
        
        if line != original:
            modified = True
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines), modified

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, modified = fix_syntax_errors(content)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 全面修复语法错误...")
    print(f"📁 目录: {commands_dir.absolute()}")
    print()
    
    fixed_count = 0
    error_count = 0
    total = len(list(commands_dir.glob("*.py")))
    
    for py_file in sorted(commands_dir.glob("*.py")):
        if fix_file(py_file):
            print(f"✅ 修复: {py_file.name}")
            fixed_count += 1
    
    print()
    print(f"📊 修复统计:")
    print(f"  总文件: {total}")
    print(f"  修复: {fixed_count}")
    print(f"  错误: {error_count}")
    
    return fixed_count > 0

if __name__ == "__main__":
    main()
