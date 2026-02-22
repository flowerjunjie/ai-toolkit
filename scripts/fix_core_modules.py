#!/usr/bin/env python3
"""
批量修复核心模块 - 基于完美模板
"""

import re
from pathlib import Path

# 需要修复的核心模块
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

def fix_module_content(file_path):
    """修复模块内容"""
    try:
        content = file_path.read_text()
        original = content
        
        # 修复规则（基于完美模板）
        
        # 1. 修复装饰器 - 确保括号闭合
        content = re.sub(
            r'@(\w+\.\w+)\.command\(name\("([^"]+)"\)(?=\s*\n)',
            r'@\1.command(name="\2")',
            content
        )
        content = re.sub(
            r'@(\w+\.\w+)\.group\(name\("([^"]+)"\)(?=\s*\n)',
            r'@\1.group(name="\2")',
            content
        )
        
        # 2. 修复 console.print(f( -> console.print(f"
        content = re.sub(r'console\.print\(f\(', 'console.print(f"', content)
        
        # 3. 修复 f("xxx") -> f"xxx"
        content = re.sub(r'=\s*f\('([^"]+)""\)', r'= f"\1""', content)
        
        # 4. 修复 help("xxx") -> help="xxx"
        content = re.sub(r'help\("([^"]+)"\)(?=[,)])', r'help="\1"', content)
        
        # 5. 修复 default("xxx") -> default="xxx"
        content = re.sub(r'default\("([^"]+)"\)(?=[,)])', r'default="\1"', content)
        
        # 6. 修复 console print ( -> console.print(
        content = re.sub(r'\s+console\s+print\s*\(', ' console.print(', content)
        
        # 7. 修复中文引号
        content = content.replace('"', '"').replace('"', '"')
        
        if content != original:
            file_path.write_text(content)
            return True
        return False
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    """主函数"""
    commands_dir = Path("src/ai_toolkit/commands")
    
    print("🔧 修复8个核心模块...\n")
    
    fixed_count = 0
    for module_name in CORE_MODULES:
        file_path = commands_dir / module_name
        if not file_path.exists():
            print(f"⚠️  {module_name} 不存在")
            continue
        
        print(f"修复: {module_name}")
        if fix_module_content(file_path):
            print(f"  ✅ 已修复")
            fixed_count += 1
        else:
            print(f"  - 无需修复")
    
    print(f"\n📊 修复了 {fixed_count} 个核心模块")
    print("\n现在验证语法...")
    
    # 验证修复结果
    still_errors = []
    for module_name in CORE_MODULES:
        file_path = commands_dir / module_name
        if file_path.exists():
            try:
                compile(file_path.read_text(), str(file_path), 'exec')
                print(f"✅ {module_name}")
            except:
                print(f"❌ {module_name} 仍有错误")
                still_errors.append(module_name)
    
    if still_errors:
        print(f"\n⚠️ 仍有 {len(still_errors)} 个模块需要手动修复")
        for name in still_errors:
            print(f"  - {name}")
    else:
        print(f"\n✅ 所有核心模块修复成功！")

if __name__ == "__main__":
    main()
