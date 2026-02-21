"""
交互式Shell模式
"""

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax
from pathlib import Path
import subprocess
import os

console = Console()


@click.command()
@click.option("--history-file", "-h", type=click.Path(), help="历史记录文件")
def shell(history_file: str):
    """进入交互式Shell模式"""
    console.print("\n🐚 AI Toolkit Shell 模式")
    console.print("输入 'help' 查看命令，'exit' 退出\n")

    history = []

    # 内置命令
    builtins = {
        "help": "显示帮助",
        "exit": "退出Shell",
        "clear": "清屏",
        "status": "系统状态",
        "version": "版本信息",
        "history": "查看历史",
    }

    while True:
        try:
            # 读取输入
            prompt_text = Prompt.ask(
                "[bold cyan]ai-toolkit[/bold cyan]",
                default="",
                show_default=False
            )

            if not prompt_text:
                continue

            prompt_text = prompt_text.strip()

            # 处理退出
            if prompt_text in ["exit", "quit", "q"]:
                console.print("👋 再见！")
                break

            # 处理清屏
            if prompt_text in ["clear", "cls"]:
                console.clear()
                continue

            # 处理帮助
            if prompt_text in ["help", "?"]:
                console.print("\n可用命令:")
                console.print("  ai-toolkit 命令 - 直接执行AI Toolkit命令")
                console.print("  " + ", ".join(builtins.keys()))
                console.print("\n示例:")
                console.print("  > models list")
                console.print("  > prompts list")
                console.print("  > exit")
                console.print("")
                continue

            # 处理状态
            if prompt_text == "status":
                from ai_toolkit.commands.cli import status

                status()
                continue

            # 处理版本
            if prompt_text == "version":
                from ai_toolkit.commands.system_cmd import system_version

                system_version()
                continue

            # 处理历史
            if prompt_text == "history":
                console.print("\n命令历史:")
                for i, cmd in enumerate(history, 1):
                    console.print(f"  {i}. {cmd}")
                console.print("")
                continue

            # 添加到历史
            history.append(prompt_text)

            # 执行命令
            if prompt_text.startswith("!"):
                # Shell命令
                shell_cmd = prompt_text[1:]
                console.print(f"\n$ {shell_cmd}")
                result = subprocess.run(
                    shell_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                )

                if result.stdout:
                    console.print(result.stdout)
                if result.stderr:
                    console.print(f"[red]{result.stderr}[/red]")

                console.print(f"返回码: {result.returncode}")
                console.print("")
            else:
                # AI Toolkit 命令
                cmd = f"ai-toolkit {prompt_text}"
                console.print(f"\n$ {cmd}")
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                )

                if result.stdout:
                    console.print(result.stdout)
                if result.stderr:
                    console.print(f"[dim]{result.stderr}[/dim]")

        except KeyboardInterrupt:
            console.print("\n👋 再见！")
            break
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")
