# 代码质量自动化检查脚本

import os
import subprocess
from pathlib import Path
from typing import List, Tuple

# 项目根目录
ROOT = Path(__file__).parent.parent

# 需要检查的文件
PYTHON_FILES = list((ROOT / "src").rglob("*.py"))

# 排除的文件
EXCLUDE = [
    "__init__.py",
    "completion.py",
    "completion.zsh",
]

def run_command(cmd: List[str], description: str) -> Tuple[int, str, str]:
    """运行命令并返回结果"""
    print(f"\n{'='*60}")
    print(f"检查: {description}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    return result.returncode, result.stdout, result.stderr

def check_type_annotations():
    """检查类型注解"""
    missing_types = []

    for py_file in PYTHON_FILES:
        if py_file.name in EXCLUDE:
            continue

        with open(py_file, "r") as f:
            content = f.read()
            lines = content.split("\n")

        in_function = False
        function_name = None

        for i, line in enumerate(lines, 1):
            # 检测函数定义
            if line.strip().startswith("def "):
                in_function = True
                function_name = line.strip().split("(")[0].replace("def ", "")
                
                # 检查是否有类型注解
                if "->" not in line:
                    missing_types.append((py_file, i, function_name))

    return missing_types

def check_docstrings():
    """检查文档字符串"""
    missing_docs = []

    for py_file in PYTHON_FILES:
        if py_file.name in EXCLUDE:
            continue

        with open(py_file, "r") as f:
            content = f.read()
            lines = content.split("\n")

        in_function = False
        function_line = 0
        function_name = None

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith("def ") and not stripped.startswith("def _"):
                in_function = True
                function_line = i
                function_name = stripped.split("(")[0].replace("def ", "")

            elif in_function:
                # 检查是否有文档字符串
                if '"""' in stripped or "'''" in stripped:
                    in_function = False
                elif stripped and not stripped.startswith("#"):
                    # 第一个非空行不是文档字符串
                    if not stripped.startswith("@"):
                        missing_docs.append((py_file, function_line, function_name))
                        in_function = False

    return missing_docs

def main():
    """主检查函数"""
    print("🔍 AI Toolkit 代码质量检查")
    print("="*60)

    # 1. 类型注解检查
    print("\n1️⃣  类型注解检查")
    missing_types = check_type_annotations()
    
    if missing_types:
        print(f"❌ 发现 {len(missing_types)} 个缺少类型注解的函数")
        for file_path, line, name in missing_types[:10]:
            print(f"   {file_path}:{line} - {name}")
    else:
        print("✅ 所有函数都有类型注解")

    # 2. 文档字符串检查
    print("\n2️⃣  文档字符串检查")
    missing_docs = check_docstrings()
    
    if missing_docs:
        print(f"❌ 发现 {len(missing_docs)} 个缺少文档字符串的函数")
        for file_path, line, name in missing_docs[:10]:
            print(f"   {file_path}:{line} - {name}")
    else:
        print("✅ 所有函数都有文档字符串")

    # 3. 运行 mypy
    print("\n3️⃣  类型检查 (mypy)")
    returncode, stdout, stderr = run_command(
        ["python3", "-m", "mypy", "src/ai_toolkit/"],
        "mypy 类型检查"
    )
    
    if returncode == 0:
        print("✅ mypy 检查通过")
    else:
        print("❌ mypy 发现问题:")
        print(stdout)

    # 4. 运行 flake8
    print("\n4️⃣  代码风格检查 (flake8)")
    returncode, stdout, stderr = run_command(
        ["python3", "-m", "flake8", "src/ai_toolkit/", "--max-line-length=100"],
        "flake8 代码检查"
    )
    
    if returncode == 0:
        print("✅ flake8 检查通过")
    else:
        print("❌ flake8 发现问题:")
        print(stdout)

    # 5. 运行 black
    print("\n5️⃣  代码格式检查 (black)")
    returncode, stdout, stderr = run_command(
        ["python3", "-m", "black", "--check", "src/", "tests/"],
        "black 格式检查"
    )
    
    if returncode == 0:
        print("✅ 代码格式正确")
    else:
        print("❌ 代码格式需要调整:")
        print(stdout)

    # 6. 运行测试
    print("\n6️⃣  运行测试")
    returncode, stdout, stderr = run_command(
        ["python3", "-m", "pytest", "tests/", "-v"],
        "pytest 测试"
    )
    
    if returncode == 0:
        print("✅ 所有测试通过")
    else:
        print("❌ 测试失败:")
        print(stdout)

    # 总结
    print("\n" + "="*60)
    print("📊 检查总结")
    print("="*60)
    
    issues = len(missing_types) + len(missing_docs)
    
    if issues == 0:
        print("✅ 代码质量优秀！")
        return 0
    else:
        print(f"⚠️  发现 {issues} 个需要改进的地方")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
