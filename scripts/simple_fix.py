#!/usr/bin/env python3
"""
简单直接的语法修复脚本
"""

import re
from pathlib import Path

def fix_file_simple(file_path):
    """简单修复"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            original = line
            
            # 修复: console.print(f("xxx") -> console.print(f"xxx")
            if 'console.print(f("' in line and '")") in line:
                line = line.replace('console.print(f("', 'console.print(f"')
                line = line.replace('")")', '")')
                modified = True
            
            # 修复: help("xxx") -> help="xxx"
            if 'help("' in line and 'default' not in line:
                line = re.sub(r'help\("([^"]+)"\)', r'help="\1"', line)
                modified = True
            
            # 修复: default("xxx") -> default="xxx"  
            if 'default("' in line:
                line = re.sub(r'(?<=default)\("([^"]+)"\)', r'="\1"', line)
                modified = True
            
            new_lines.append(line)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True
        return False
    except Exception as e:
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 简单语法修复...")
    
    fixed_count = 0
    for py_file in sorted(commands_dir.glob("*.py")):
        if fix_file_simple(py_file):
            print(f"✅ {py_file.name}")
            fixed_count += 1
    
    print(f"\n✅ 修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
