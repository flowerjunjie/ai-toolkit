#!/usr/bin/env python3
"""
核心模块识别和优先级修复
"""

import re
from pathlib import Path

def check_syntax(file_path):
    """检查文件语法"""
    try:
        compile(file_path.read_text(), str(file_path), 'exec')
        return True
    except:
        return False

def get_all_modules():
    """获取所有模块"""
    commands_dir = Path("src/ai_toolkit/commands")
    modules = {}
    
    for py_file in commands_dir.glob("*.py"):
        if py_file.name.startswith('_'):
            continue
        
        is_valid = check_syntax(py_file)
        modules[py_file.name] = {
            'path': py_file,
            'valid': is_valid,
            'size': py_file.stat().st_size
        }
    
    return modules

def prioritize_modules(modules):
    """确定优先级"""
    # 核心模块（高优先级）
    core_modules = [
        'ai_core.py', 'nlp_core.py', 'cv_core.py', 'ml_core.py',
        'data_processing.py', 'database.py', 'api.py',
        'dev_tools.py', 'git_tools.py', 'docker_tools.py',
        'aws.py', 'azure.py', 'gcp.py',
        'medical.py', 'ecommerce.py', 'edtech.py',
        'blockchain.py', 'crypto.py', 'trading.py',
        'super.py'
    ]
    
    prioritized = []
    other = []
    
    for name in core_modules:
        if name in modules:
            prioritized.append((name, modules[name]))
    
    for name, info in modules.items():
        if name not in core_modules:
            other.append((name, info))
    
    return prioritized, other

def main():
    """主函数"""
    print("🔍 分析模块状态...\n")
    
    modules = get_all_modules()
    core, other = prioritize_modules(modules)
    
    print(f"📊 总模块: {len(modules)}")
    print(f"✅ 语法正确: {sum(1 for m in modules.values() if m['valid'])}")
    print(f"❌ 语法错误: {sum(1 for m in modules.values() if not m['valid'])}")
    print()
    
    print("🎯 核心模块优先级修复:")
    print("=" * 60)
    
    for i, (name, info) in enumerate(core[:20], 1):
        status = "✅" if info['valid'] else "❌"
        print(f"{i:2}. {status} {name:30} {info['size']/1024:.1f}KB")
    
    print()
    print("📋 其他模块（按优先级）:")
    print("=" * 60)
    
    valid_other = [n for n, i in other if i['valid']]
    invalid_other = [n for n, i in other if not i['valid']]
    
    print(f"✅ 正常: {len(valid_other)} 个")
    print(f"❌ 需修复: {len(invalid_other)} 个")
    
    if invalid_other:
        print(f"\n前10个待修复:")
        for i, name in enumerate(invalid_other[:10], 1):
            print(f"  {i}. {name}")
    
    print()
    print("💡 修复建议:")
    print("  1. 先修复20个核心模块")
    print("  2. 确保核心功能可用")
    print("  3. 逐步修复其他模块")

if __name__ == "__main__":
    main()
