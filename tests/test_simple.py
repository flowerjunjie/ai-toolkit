"""
简单的模块测试 - 测试核心模块
"""

import ast
from pathlib import Path


def test_module_syntax():
    """测试模块语法"""
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = list(commands_dir.glob('*.py'))
    
    # 排除__开头的文件
    py_files = [f for f in py_files if not f.name.startswith('_')]
    
    print(f"🧪 测试 {len(py_files)} 个模块...\n")
    
    passed = 0
    failed = []
    
    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
            passed += 1
        except SyntaxError as e:
            failed.append((py_file.name, e.lineno, e.msg))
    
    print(f"✅ 通过: {passed}/{len(py_files)}")
    
    if failed:
        print(f"\n❌ 失败:")
        for name, line, error in failed:
            print(f"  {name}:{line} - {error}")
        return False
    
    return True


def test_module_imports():
    """测试模块导入"""
    import sys
    sys.path.insert(0, 'src')
    
    # 测试几个核心模块
    test_modules = [
        'simple_core',
        'api',
        'shell',
        'guide',
    ]
    
    print(f"\n🧪 测试模块导入...\n")
    
    passed = 0
    for module in test_modules:
        try:
            exec(f"from ai_toolkit.commands.{module} import *")
            print(f"  ✓ {module}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {module}: {e}")
    
    print(f"\n✅ 导入测试: {passed}/{len(test_modules)}")
    
    return passed == len(test_modules)


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 AI Toolkit 测试套件")
    print("=" * 50)
    
    # 测试1: 语法测试
    print("\n📋 测试1: 语法检查")
    syntax_ok = test_module_syntax()
    
    # 测试2: 导入测试
    print("\n📋 测试2: 模块导入")
    import_ok = test_module_imports()
    
    # 总结
    print("\n" + "=" * 50)
    if syntax_ok and import_ok:
        print("✅ 所有测试通过！")
        print("=" * 50)
    else:
        print("❌ 部分测试失败")
        print("=" * 50)
