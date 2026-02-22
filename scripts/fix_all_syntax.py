#!/usr/bin/env python3
"""
全面修复Python文件语法错误
"""

import re
from pathlib import Path

def fix_all_syntax_issues(file_path):
    """修复所有语法问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    original = content
    changes = 0
    
    # 修复1: @click.group(name="xxx") -> @click.group(name="xxx")
    content = re.sub(r'(@click\.group\(name\("([^"]+)"\))', 
                    r'@\1', content)
    
    # 修复2: @click.command(name("xxx") -> @click.command(name="xxx")
    content = re.sub(r'(@click\.command\(name\("([^"]+)"\))', 
                    r'@\1', content)
    
    # 修复3: 修复 console.print(f( -> console.print(f"
    content = re.sub(r'console\.print\(f\("([^"]*)"\)', 
                    r'console.print(f"\1"', content)
    
    # 修复4: 修复 f("xxx") -> f"xxx"
    content = re.sub(r'=\s+f\("([^"]+)"\)', 
                    r'= f"\1"', content)
    
    # 修复5: 修复 help("xxx") -> help="xxx"
    content = re.sub(r'help\("([^"]+)"\)', r'help="\1"', content)
    
    # 修复6: 修复 default("xxx") -> default="xxx"  
    content = re.sub(r'default\("([^"]+)"\)', r'default="\1"', content)
    
    # 修复7: 修复 choice("xxx") -> choice="xxx"
    content = re.sub(r'choice\("([^"]+)"\)', r'choice="\1"', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 开始修复语法错误...")
    fixed_count = 0
    error_count = 0
    
    for py_file in commands_dir.glob("*.py"):
        try:
            if fix_all_syntax_issues(py_file):
                print(f"✅ 修复: {py_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ 错误: {py_file.name} - {e}")
            error_count += 1
    
    print(f"\n📊 修复统计:")
    print(f"  修复: {fixed_count} 个文件")
    print(f"  错误: {error_count} 个文件")

if __name__ == "__main__":
    main()
