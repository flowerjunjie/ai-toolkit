"""
更新命令 - 检查并更新到最新版本
"""

import click
import requests
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command(name="upgrade")
def upgrade_command():
    """检查并更新到最新版本"""
    console.print("🔄 检查更新...")

    try:
        # 从 PyPI 获取最新版本
        response = requests.get("https://pypi.org/pypi/ai-toolkit/json", timeout=5)
        response.raise_for_status()

        data = response.json()
        latest_version = data["info"]["version"]
        current_version = "0.1.0"

        console.print(f"当前版本: [cyan]{current_version}[/cyan]")
        console.print(f"最新版本: [cyan]{latest_version}[/cyan]")

        if latest_version > current_version:
            console.print(
                Panel(
                    f"[yellow]发现新版本: {latest_version}[/yellow]\n\n"
                    f"更新命令:\n"
                    f"[cyan]pip install --upgrade ai-toolkit[/cyan]",
                    title="📦 更新可用",
                    border_style="yellow",
                )
            )

            if click.confirm("是否现在更新？"):
                console.print("正在更新...")
                import subprocess

                subprocess.run(["pip", "install", "--upgrade", "ai-toolkit"], check=True)
                console.print("[green]✅ 更新完成![/green]")
        else:
            console.print("[green]✅ 已是最新版本[/green]")

    except Exception as e:
        console.print(f"[red]检查更新失败: {e}[/red]")
