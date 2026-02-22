"""
测试命令
"""

import click
import subprocess
from rich.console import Console
from rich.progress import Progress
from pathlib import Path
import time

console = Console()


@click.group(name="test")
def test_cli():
    """测试相关命令"""
    pass


@test_cli.command(name="all")
@click.option("--verbose", "-v", is_flag=True, help="详细输出")
@click.option("--coverage", "-c", is_flag=True, help="生成覆盖率报告")
def test_all(verbose: bool, coverage: bool):
    """运行所有测试"""
    console.print("\n🧪 运行测试套件\n")

    cmd = ["python3", "-m", "pytest", "tests/", "-v"]

    if coverage:
        cmd.extend(["--cov=src/ai_toolkit", "--cov-report=html"])

    console.print(f"命令: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=Path.cwd())

    if result.returncode == 0:
        console.print("\n[green]✅ 所有测试通过！[/green]")
    else:
        console.print(f"\n[red]❌ 测试失败，返回码: {result.returncode}[/red]")


@test_cli.command(name="unit"
@click.argument("name", required=False)
@click.option("--verbose", "-v", is_flag=True)
def test_unit(name: str, verbose: bool):
    """运行单元测试"""
    if name:
        console.print(f"🧪 运行测试: {name}\n")
        cmd = ["python3", "-m", "pytest", f"tests/test_{name}.py", "-v"]
    else:
        console.print("🧪 运行所有单元测试\n")
        cmd = ["python3", "-m", "pytest", "tests/", "-v", "-k", "not integration"]

    console.print(f"命令: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=Path.cwd())

    if result.returncode == 0:
        console.print("\n[green]✅ 测试通过！[/green]")
    else:
        console.print(f"\n[red]❌ 测试失败[/red]")


@test_cli.command(name="lint")
def test_lint():
    """代码检查"""
    console.print("\n🔍 代码检查\n")

    # Black
    console.print("1️⃣  代码格式...")
    result = subprocess.run(
        ["python3", "-m", "black", "--check", "src/", "tests/"],
        cwd=Path.cwd(),
    )

    if result.returncode == 0:
        console.print("   [green]✅ 代码格式正确[/green]")
    else:
        console.print("   [yellow]⚠️  代码需要格式化: black src/ tests/[/yellow]")

    # isort
    console.print("\n2️⃣  导入排序...")
    result = subprocess.run(
        ["python3", "-m", "isort", "--check-only", "src/", "tests/"],
        cwd=Path.cwd(),
    )

    if result.returncode == 0:
        console.print("   [green]✅ 导入排序正确[/green]")
    else:
        console.print("   [yellow]⚠️  导入需要排序: isort src/ tests/[/yellow]")

    # mypy (可选)
    console.print("\n3️⃣  类型检查...")
    result = subprocess.run(
        ["python3", "-m", "mypy", "src/ai_toolkit/"],
        cwd=Path.cwd(),
    )

    if result.returncode == 0:
        console.print("   [green]✅ 类型检查通过[/green]")
    else:
        console.print("   [yellow]⚠️️ 有类型问题（可选修复）[/yellow]")

    console.print("\n" + "="*60)
    console.print("💡 修复建议:")
    console.print("   black src/ tests/          # 格式化代码")
    console.print("   isort src/ tests/           # 排序导入")
    console.print("   mypy src/ai_toolkit/        # 类型检查")


@test_cli.command(name="fix")
def test_fix():
    """自动修复代码问题"""
    console.print("\n🔧 自动修复\n")

    # Black
    console.print("1️⃣ 格式化代码...")
    result = subprocess.run(
        ["python3", "-m", "black", "src/", "tests/"],
        cwd=Path.cwd(),
    )

    if result.returncode == 0:
        console.print("   ✅ 格式化完成")
    else:
        console.print("   ❌ 格式化失败")

    # isort
    console.print("\n2️⃣  排序导入...")
    result = subprocess.run(
        ["python3", "-m", "isort", "src/", "tests/"],
        cwd=Path.cwd(),
    )

    if result.returncode == 0:
        console.print("   ✅ 排序完成")
    else:
        console.print("   ❌ 排序失败")

    console.print("\n✅ 代码已自动修复！")


@test_cli.command(name="watch")
def test_watch():
    """监听模式（文件改动自动测试）"""
    console.print("\n👀️ 监听模式（文件改动自动测试）")
    console.print("按 Ctrl+C 停止\n")

    try:
        while True:
            subprocess.run(
                ["python3", "-m", "pytest", "tests/", "-v"],
                cwd=Path.cwd(),
            )
            console.print("\n💤 等待文件改动...\n")
            time.sleep(5)
    except KeyboardInterrupt:
        console.print("\n[yellow]监听已停止[/yellow]")


@test_cli.command(name="add")
@click.argument("test_name")
@click.option("--test", "-t", help="测试内容")
def add_test(test_name: str, test: str):
    """添加新测试"""
    test_file = Path("tests") / f"test_{test_name}.py"

    console.print(f"📝 创建测试: {test_file}\n")

    # 测试模板
    if not test:
        test = "// 在这里写测试"

    template = f'''"""
\"\"\"
{test_name} 测试
\"\"\"

import pytest


class Test{test_name.capitalize()}:
    def test_something():
        assert True
'''
    
    if test:
        template = f'''"""
def test_{test_name}():
    {test}
'''

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(template)

    console.print(f"✅ 测试文件已创建: {test_file}")
    console.print(f"\n编辑文件，然后运行: ai-toolkit test test {test_name}")
