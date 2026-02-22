#!/usr/bin/env python3
"""
简单高效的修复脚本
"""

import re
from pathlib import Path

CORE_MODULES = [
    'data_processing.py',
    'api.py', 
    'dev_tools.py',
    'medical.py',
    'ecommerce.py',
    'edtech.py',
    'blockchain.py',
    'super.py'
]

def fix_file(file_path):
    """修复文件"""
    try:
        content = file_path.read_text()
        original = content
        
        # 修复1: 装饰器括号
        content = re.sub(r'@(\w+)\.command\(name\("([^"]+)"\)', r'@\1.command(name="\2")', content)
        content = re.sub(r'@(\w+)\.group\(name\("([^"]+)"\)', r'@\1.group(name="\2")', content)
        
        # 修复2: console.print(f(
        content = content.replace('console.print(f(', 'console.print(f"')
        
        # 修复3: console print (
        content = content.replace('console print(', 'console.print(')
        
        # 修复4: 中文引号
        content = content.replace('"', '"').replace('"', '"')
        
        if content != original:
            file_path.write_text(content)
            return True
        return False
    except Exception as e:
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("修复核心模块...\n")
    
    fixed = 0
    for name in CORE_MODULES:
        path = commands_dir / name
        if path.exists():
            if fix_file(path):
                print(f"✅ {name}")
                fixed += 1
    
    print(f"\n修复了 {fixed} 个模块")

if __name__ == "__main__":
    main()
