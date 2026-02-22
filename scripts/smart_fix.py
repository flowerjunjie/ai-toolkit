#!/usr/bin/env python3
"""
智能修复 - 识别并修复各种语法错误
"""

import re
from pathlib import Path

def fix_all_issues(content):
    """修复所有问题"""
    lines = content.split('\n')
    result = []
    in_string = False
    string_char = '"'
    
    for i, line in enumerate(lines):
        # 跳过注释
        if line.strip().startswith('#'):
            result.append(line)
            continue
        
        # 修复未闭合的f-string
        if 'console.print(f"' in line and '")")' not in line:
            # 尝试修复
            line = line.replace('console.print(f(', 'console.print(f"')
            line = line.replace('console.print(f"', 'console.print(f"')
        
        # 修复: f("xxx") -> f"xxx"  
        if '=(' in line and 'f("' in line:
            line = re.sub(r'=\s*f\('([^"]+)""\)', r'= f"\1""', line)
        
        # 修复: 类型提示中的括号问题
        line = re.sub(r'def ([^(]+)\([^)]*)\):', r'def \1\2):', line)
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 智能修复所有语法问题...\n")
    
    fixed_count = 0
    for py_file in sorted(commands_dir.glob("*.py")):
        try:
            content = py_file.read_text()
            fixed = fix_all_issues(content)
            
            if fixed != content:
                py_file.write_text(fixed)
                print(f"✅ {py_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ {py_file.name}: {e}")
    
    print(f"\n✅ 处理完成")

if __name__ == "__main__":
    main()
