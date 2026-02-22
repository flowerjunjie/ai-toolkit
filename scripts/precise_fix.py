#!/usr/bin/env python3
"""
精确修复脚本 - 修复装饰器语法错误
"""

import re
from pathlib import Path

def fix_decorator_syntax(content):
    """修复装饰器语法"""
    lines = content.split('\n')
    result = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查未闭合的装饰器
        if re.match(r'@\w+\.\w+\([^\)]*$', line):
            # 检查下一行是否是函数定义
            if i + 1 < len(lines) and 'def ' in lines[i + 1]:
                # 修复当前行：添加闭合括号
                if not line.rstrip().endswith(')'):
                    line = line.rstrip() + ')'
        
        # 修复 console.print(f(" -> console.print(f"
        line = re.sub(r'console\.print\(f\(', 'console.print(f"', line)
        
        # 修复 console print ( -> console.print(
        line = re.sub(r'console\s+print\s*\(', 'console.print(', line)
        
        # 修复 f("xxx") -> f"xxx"
        line = re.sub(r'=\s*f\(\)', r'= f"', line)
        
        # 修复 help("xxx") -> help="xxx"
        line = re.sub(r'help\("([^"]+)"\)(?=[,)])', r'help="\1"', line)
        
        # 修复 default("xxx") -> default="xxx"
        line = re.sub(r'default\("([^"]+)"\)(?=[,)])', r'default="\1"', line)
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def fix_file(file_path):
    """修复单个文件"""
    try:
        content = file_path.read_text(encoding='utf-8')
        fixed = fix_decorator_syntax(content)
        
        if fixed != content:
            file_path.write_text(fixed, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 精确修复装饰器语法...\n")
    
    # 找出所有需要修复的文件
    error_files = []
    for py_file in commands_dir.glob("*.py"):
        try:
            compile(py_file.read_text(), str(py_file), 'exec')
        except SyntaxError:
            error_files.append(py_file)
    
    print(f"找到 {len(error_files)} 个需要修复的文件\n")
    
    fixed_count = 0
    for file_path in error_files:
        print(f"修复: {file_path.name}")
        if fix_file(file_path):
            print(f"  ✅ 已修复")
            fixed_count += 1
        else:
            print(f"  - 无变化")
    
    print(f"\n✅ 修复了 {fixed_count} 个文件")
    
    # 验证修复结果
    remaining = []
    for file_path in error_files:
        try:
            compile(file_path.read_text(), str(file_path), 'exec')
        except SyntaxError:
            remaining.append(file_path.name)
    
    if remaining:
        print(f"\n⚠️ 仍有 {len(remaining)} 个文件需要手动修复")
        for name in remaining[:10]:
            print(f"  - {name}")
    else:
        print(f"\n✅ 所有文件修复成功！")

if __name__ == "__main__":
    main()
