"""
Web UI 命令
"""

import click
import threading
import time
from rich.console import Console

from ai_toolkit.web.app import start_server

console = Console()


@click.command()
@click.option("--host", "-h", default="0.0.0.0", help="主机地址")
@click.option("--port", "-p", default=8000, help="端口号")
@click.option("--detach", "-d", is_flag=True, help="后台运行")
def webui(host: str, port: int, detach: bool):
    """启动Web UI服务器"""
    console.print(f"🌐 启动 AI Toolkit Web UI")
    console.print(f"地址: [cyan]http://{host}:{port}[/cyan]")
    console.print(f"按 Ctrl+C 停止服务器\n")

    if detach:
        # 后台运行
        import subprocess

        subprocess.Popen(
            ["python3", "-m", "ai_toolkit.web.app"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        console.print(f"✅ Web UI 已在后台启动")
        console.print(f"访问: http://{host}:{port}")
    else:
        # 前台运行
        try:
            start_server(host, port)
        except KeyboardInterrupt:
            console.print("\n[yellow]Web UI 已停止[/yellow]")
