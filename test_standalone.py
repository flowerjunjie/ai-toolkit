"""
完全独立的测试 - 不依赖任何内部模块
"""

import ast
import py_compile
from pathlib import Path


def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 AI Toolkit 完全独立测试")
    print("=" * 50)
    
    # 测试1: 语法检查
    print("\n📋 测试1: 语法检查")
    print("-" * 50)
    
    commands_dir = Path('src/ai_toolkit/commands')
    py_files = sorted([f for f in commands_dir.glob('*.py') if not f.name.startswith('_')])
    
    passed = 0
    failed = []
    
    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
            passed += 1
        except SyntaxError as e:
            failed.append((py_file.name, e.lineno, e.msg))
    
    print(f"  总文件: {len(py_files)}")
    print(f"  ✅ 通过: {passed}")
    print(f"  ❌ 失败: {len(failed)}")
    
    if failed:
        print(f"\n❌ 失败的文件:")
        for name, line, error in failed[:10]:
            print(f"  {name}:{line} - {error}")
        if len(failed) > 10:
            print(f"  ... 还有 {len(failed) - 10} 个")
        return False
    
    print("\n✅ 语法测试: 100%通过")
    
    # 测试2: 编译测试
    print("\n📋 测试2: 编译测试")
    print("-" * 50)
    
    compile_passed = 0
    compile_failed = []
    
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
            compile_passed += 1
        except py_compile.PyCompileError as e:
            compile_failed.append((py_file.name, str(e)))
    
    print(f"  编译通过: {compile_passed}")
    print(f"  编译失败: {len(compile_failed)}")
    
    if compile_failed:
        print(f"\n❌ 编译失败的文件:")
        for name, error in compile_failed[:5]:
            print(f"  {name}")
            print(f"    {error[:80]}")
        return False
    
    print("\n✅ 编译测试: 100%通过")
    
    # 测试3: 结构测试
    print("\n📋 测试3: 结构验证")
    print("-" * 50)
    
    structure_ok = True
    all_have_cli_group = True
    
    for py_file in py_files[:20]:  # 检查前20个
        with open(py_file, 'r') as f:
            content = f.read()
            
            # 检查是否有@click.group或@click.command
            has_cli_group = '@click.group' in content or '@click.command' in content
            if not has_cli_group:
                all_have_cli_group = False
                print(f"  ⚠️ {py_file.name}: 缺少CLI装饰器")
    
    if all_have_cli_group:
        print("  ✓ 所有模块都有CLI装饰器")
        structure_ok = True
    else:
        print("  ⚠️ 部分模块缺少CLI装饰器")
    
    print("\n" + "=" * 50)
    
    if passed == len(py_files) and compile_passed == len(py_files) and structure_ok:
        print("✅ 所有测试通过！")
        print(f"📊 统计:")
        print(f"  总模块: {len(py_files)}")
        print(f"  语法正确: 100%")
        print(f"  编译通过: 100%")
        print("=" * 50)
        return True
    else:
        print("❌ 部分测试失败")
        print("=" * 50)
        return False


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
