#!/usr/bin/env python3
"""
逐个文件修复 - 精确定位并修复
"""

import re
from pathlib import Path

ERROR_PATTERNS = [
    (r'console\.print\(f\("([^"]*)"\)', r'console.print(f"\1")'),  # console.print(f("xxx")
    (r'=\s*f\('([^"]+)""\)', r'= f"\1""'),  # f("xxx")
    (r'help\("([^"]+)"\)(?=[,)])', r'help="\1"'),  # help("xxx")
    (r'default\("([^"]+)"\)(?=[,)])', r'default="\1"'),  # default("xxx")
]

def fix_line(line):
    """修复单行"""
    original = line
    
    for pattern, replacement in ERROR_PATTERNS:
        line = re.sub(pattern, replacement, line)
    
    return line if line != original else original

def fix_python_file(file_path):
    """修复Python文件"""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        fixed_lines = []
        for line in lines:
            # 跳过空行和注释
            if not line.strip() or line.strip().startswith('#'):
                fixed_lines.append(line)
                continue
            
            # 修复行
            fixed_lines.append(fix_line(line))
        
        fixed_content = '\n'.join(fixed_lines)
        
        if fixed_content != content:
            file_path.write_text(fixed_content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        return False

def verify_file(file_path):
    """验证文件语法"""
    try:
        compile(file_path.read_text(), str(file_path), 'exec')
        return True
    except:
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 逐个文件修复...\n")
    
    # 找出所有有错误的文件
    error_files = []
    for py_file in commands_dir.glob("*.py"):
        if not verify_file(py_file):
            error_files.append(py_file)
    
    print(f"找到 {len(error_files)} 个问题文件\n")
    
    fixed_count = 0
    still_error = []
    
    for file_path in error_files[:20]:  # 先修复前20个
        print(f"修复: {file_path.name}")
        
        if fix_python_file(file_path):
            print(f"  ✅ 已修复")
            fixed_count += 1
            
            if verify_file(file_path):
                print(f"  ✅ 验证通过")
            else:
                print(f"  ⚠️ 仍有问题")
                still_error.append(file_path.name)
        else:
            print(f"  - 修复失败")
            still_error.append(file_path.name)
    
    print(f"\n📊 第一轮修复:")
    print(f"  处理: 20个文件")
    print(f"  修复: {fixed_count}个")
    print(f"  失败: {len(still_error)}个")
    
    if still_error:
        print(f"\n⚠️ 仍需修复: {len(still_error)} 个")

if __name__ == "__main__":
    main()
