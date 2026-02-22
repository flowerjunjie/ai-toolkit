#!/usr/bin/env python3
"""
终极修复脚本 - 修复所有已知问题
"""

import re
from pathlib import Path

def fix_content(content):
    """修复内容"""
    lines = content.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        # 跳过注释行
        if line.strip().startswith('#'):
            result.append(line)
            continue
        
        # 修复1: 装饰器未闭合括号
        if re.search(r'@\w+\.\w+\([^\)]*$', line):
            # 检查下一行是否是函数定义
            if i + 1 < len(lines) and 'def ' in lines[i + 1]:
                # 添加闭合括号
                line = line.rstrip() + ')'
        
        # 修复2: console.print(f( -> console.print(f"
        line = re.sub(r'console\.print\(f\(', 'console.print(f"', line)
        
        # 修复3: 修复  console print ( -> console.print(
        line = re.sub(r'\s+console\s+print\s*\(', ' console.print(', line)
        
        # 修复4: f("xxx") -> f"xxx"
        line = re.sub(r'=\s*f\("([^"]+)""\)', r'= f"\1""', line)
        
        # 修复5: help("xxx") -> help="xxx"
        line = re.sub(r'help\("([^"]+)"\)(?=[,)])', r'help="\1"', line)
        
        # 修复6: default("xxx") -> default="xxx"
        line = re.sub(r'default\("([^"]+)"\)(?=[,)])', r'default="\1"', line)
        
        # 修复7: 中文引号
        line = line.replace('"', '"').replace('"', '"')
        
        result.append(line)
    
    return '\n'.join(result)

def fix_file(file_path):
    """修复文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed = fix_content(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        
        return True
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 终极修复...")
    print()
    
    count = 0
    for py_file in sorted(commands_dir.glob("*.py")):
        if fix_file(py_file):
            count += 1
    
    print(f"✅ 处理了 {count} 个文件")
    print()
    print("现在运行语法检查...")
    
    # 运行语法检查
    errors = []
    for py_file in commands_dir.glob("*.py"):
        try:
            compile(py_file.read_text(), str(py_file), 'exec')
        except SyntaxError as e:
            errors.append((py_file.name, e))
    
    if errors:
        print(f"❌ 仍有 {len(errors)} 个文件有错误:")
        for name, err in errors[:10]:
            print(f"  - {name}: {err}")
    else:
        print("✅ 所有文件语法正确！")

if __name__ == "__main__":
    main()
