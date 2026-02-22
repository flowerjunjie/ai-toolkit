#!/usr/bin/env python3
"""
简单逐个修复
"""

from pathlib import Path

def fix_line(line):
    """修复一行"""
    # 修复 console.print(f( -> console.print(f"
    line = line.replace('console.print(f(', 'console.print(f"')
    line = line.replace('console.print(f"', 'console.print(f"')
    
    # 修复 f("xxx") -> f"xxx"
    line = line.replace('= f("', '= f"')
    
    return line

def fix_file(path):
    """修复文件"""
    try:
        text = path.read_text()
        lines = text.split('\n')
        fixed = [fix_line(line) for line in lines]
        
        new_text = '\n'.join(fixed)
        if new_text != text:
            path.write_text(new_text)
            return True
        return False
    except:
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("修复20个核心文件...\n")
    
    # 核心文件列表
    core = [
        'ai_core.py', 'nlp_core.py', 'data_processing.py',
        'dev_tools.py', 'api.py', 'medical.py', 'ecommerce.py',
        'blockchain.py', 'super.py', 'iot.py'
    ]
    
    fixed = 0
    for name in core:
        path = commands_dir / name
        if path.exists():
            print(f"修复: {name}")
            if fix_file(path):
                print(f"  ✅ 已修复")
                fixed += 1
    
    print(f"\n✅ 修复了 {fixed} 个文件")

if __name__ == "__main__":
    main()
