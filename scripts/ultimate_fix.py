#!/usr/bin/env python3
"""
终极语法修复脚本 - 修复所有常见的语法错误
"""

import re
from pathlib import Path

def fix_python_syntax(content):
    """修复Python语法错误"""
    
    # 修复1: 未闭合的装饰器参数
    # @xxx.command(name="yyy" -> @xxx.command(name="yyy")
    content = re.sub(r'@(\w+)\.(command|group)\(name\("([^"]+)"\)(?=\s*\n)', 
                    r'@\1.\2(name="\3")', content)
    
    # 修复2: 修复未闭合的括号在装饰器中
    content = re.sub(r'(@\w+\.\w+\([^\)]*\)(?=\n)', 
                    lambda m: m.group(1) + ')' if not m.group(1).endswith(')') else m.group(1), 
                    content)
    
    # 修复3: console.print(f("xxx") -> console.print(f"xxx")
    content = re.sub(r'console\.print\(f\("([^"]*)"\)', 
                    r'console.print(f"\1")', content)
    
    # 修复4: 修复 f("xxx") -> f"xxx"
    content = re.sub(r'=\s*f\("([^"]+)"\)', 
                    r'= f"\1"', content)
    
    # 修复5: 修复 help("xxx") -> help="xxx"
    content = re.sub(r'help\("([^"]+)"\)(?=[,)])', 
                    r'help="\1"', content)
    
    # 修复6: 修复 default("xxx") -> default="xxx"
    content = re.sub(r'default\("([^"]+)"\)(?=[,)])', 
                    r'default="\1"', content)
    
    # 修复7: 修复 choice("xxx", "yyy") -> choice=["xxx", "yyy"]
    content = re.sub(r'choice\("([^"]+)",\s*"([^"]+)"\)', 
                    r'choice=["\1", "\2"]', content)
    
    # 修复8: 修复 type("xxx") -> type="xxx"
    content = re.sub(r'(?<=\s)type\("([^"]+)"\)(?=[,)])', 
                    r'type="\1"', content)
    
    # 修复9: 修复 中文字符串的引号问题
    content = re.sub(r'([=\(,\[])\s*「([^」]*)」', 
                    r'\1"\2"', content)
    
    # 修复10: 修复 console print ( -> console.print(
    content = re.sub(r'console print\(', 
                    'console.print(', content)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_python_syntax(content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ 错误处理 {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 终极语法修复...")
    print(f"📁 目录: {commands_dir}")
    print(f"📄 文件数: {len(list(commands_dir.glob('*.py')))}")
    print()
    
    fixed_count = 0
    total_count = 0
    
    for py_file in sorted(commands_dir.glob("*.py")):
        total_count += 1
        if fix_file(py_file):
            print(f"✅ 修复: {py_file.name}")
            fixed_count += 1
    
    print()
    print(f"📊 修复统计:")
    print(f"  总文件: {total_count}")
    print(f"  修复: {fixed_count}")
    print(f"  跳过: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
