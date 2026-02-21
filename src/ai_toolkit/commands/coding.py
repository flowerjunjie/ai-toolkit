"""
AI 编码助手命令 - 使用 LLM 帮助编码
"""

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from ai_toolkit.core.api_manager import get_api_manager
from ai_toolkit.core.llm_client import LLMClient

console = Console()


@click.group(name="coding")
def coding_cli():
    """AI 编码助手 - 使用多个 LLM 提供商"""
    pass


@coding_cli.command(name="generate")
@click.argument("prompt")
@click.option("--provider", "-p", help="指定提供商 (bigmodel/minimax/kimi/doubao)")
@click.option("--output", "-o", type=click.Path(), help="输出文件")
@click.option("--model", help="指定模型（覆盖默认）")
def generate_code(prompt: str, provider: str, output: str, model: str):
    """使用 AI 生成代码"""
    console.print(f"🤖 AI 编码助手")
    console.print(f"💬 Prompt: {prompt}\n")

    try:
        client = LLMClient(provider=provider)

        # 系统提示词
        system_prompt = """你是一个专业的程序员助手。
请根据用户的需求生成高质量的代码。
代码应该：
1. 符合最佳实践
2. 包含必要的注释
3. 处理错误情况
4. 易于理解和维护

只输出代码，不要有其他解释。"""

        # 生成代码
        console.print("[dim]正在生成代码...[/dim]\n")

        if model:
            # 覆盖模型
            api_key = client.get_api_key()
            original_model = api_key.model
            api_key.model = model

        code = client.generate_with_system(
            system_prompt=system_prompt,
            user_prompt=prompt,
            max_tokens=2000,
            temperature=0.3,
        )

        if model:
            api_key.model = original_model

        # 显示代码
        console.print(
            Panel(
                Syntax(code, "python", line_numbers=True, theme="monokai"),
                title="✨ 生成的代码",
                border_style="green",
            )
        )

        # 保存到文件
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(code)

            console.print(f"\n✅ 代码已保存到: {output_path}")

    except Exception as e:
        console.print(f"[red]生成失败: {e}[/red]")


@coding_cli.command(name="review")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--provider", "-p", help="指定提供商")
def review_code(file_path: str, provider: str):
    """代码审查"""
    console.print(f"🔍 代码审查")
    console.print(f"📄 文件: {file_path}\n")

    try:
        # 读取代码
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        client = LLMClient(provider=provider)

        system_prompt = """你是一个专业的代码审查员。
请审查以下代码，指出：
1. 潜在的 bug
2. 性能问题
3. 安全问题
4. 代码风格问题
5. 改进建议

请具体、建设性地提出意见。"""

        user_prompt = f"""请审查以下代码：

```python
{code}
```"""

        console.print("[dim]正在分析代码...[/dim]\n")

        review = client.generate_with_system(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.5,
        )

        console.print(
            Panel(
                review,
                title="📋 审查结果",
                border_style="yellow",
            )
        )

    except Exception as e:
        console.print(f"[red]审查失败: {e}[/red]")


@coding_cli.command(name="explain")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--provider", "-p", help="指定提供商")
def explain_code(file_path: str, provider: str):
    """解释代码"""
    console.print(f"📖 代码解释")
    console.print(f"📄 文件: {file_path}\n")

    try:
        # 读取代码
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        client = LLMClient(provider=provider)

        system_prompt = """你是一个专业的编程老师。
请用通俗易懂的语言解释代码的功能、逻辑和设计思路。
适合初学者理解。"""

        user_prompt = f"""请解释以下代码：

```python
{code}
```"""

        console.print("[dim]正在生成解释...[/dim]\n")

        explanation = client.generate_with_system(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.5,
        )

        console.print(
            Panel(
                explanation,
                title="💡 代码解释",
                border_style="cyan",
            )
        )

    except Exception as e:
        console.print(f"[red]解释失败: {e}[/red]")


@coding_cli.command(name="status")
def api_status():
    """显示 API Key 状态"""
    api_manager = get_api_manager()

    console.print("\n🔑 API Key 状态\n")

    from rich.table import Table

    table = Table(show_header=True)
    table.add_column("提供商", style="cyan")
    table.add_column("模型", style="green")
    table.add_column("状态", style="yellow")
    table.add_column("请求数", style="blue")
    table.add_column("错误数", style="red")

    status_list = api_manager.get_status()

    for status in status_list:
        provider = status["provider"]
        model = status["model"]
        available = "✅ 可用" if status["available"] else "❌ 不可用"
        request_count = status["request_count"]
        error_count = status["error_count"]

        table.add_row(
            provider,
            model,
            available,
            str(request_count),
            str(error_count),
        )

    console.print(table)

    console.print(f"\n总计: {api_manager.get_total_count()} 个 API Key")
    console.print(f"可用: {api_manager.get_available_count()} 个")
