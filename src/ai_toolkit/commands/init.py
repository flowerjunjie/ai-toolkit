"""
初始化命令 - 交互式配置向导
"""

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from ai_toolkit.core.config import Config, save_config
from ai_toolkit.utils.helpers import check_ollama_connection

console = Console()


@click.command(name="init")
def init_command():
    """初始化 AI Toolkit 配置"""
    console.print(
        """
[bold cyan]🤖 欢迎使用 AI Toolkit![/bold cyan]

让我帮你完成初始化配置...
    """
    )

    # 1. 检查 Ollama
    console.print("\n[bold]1️⃣  检查 Ollama[/bold]")
    ollama_url = Prompt.ask("Ollama 服务地址", default="http://localhost:11434")

    console.print(f"检查连接: [dim]{ollama_url}[/dim]")

    if check_ollama_connection(ollama_url):
        console.print("[green]✅ Ollama 连接成功![/green]")
    else:
        console.print("[yellow]⚠️  Ollama 未运行[/yellow]")
        console.print("[dim]安装: https://ollama.ai[/dim]")
        console.print("[dim]启动: ollama serve[/dim]")

        if not Confirm.ask("是否继续配置？", default=True):
            console.print("[yellow]已取消[/yellow]")
            return

    # 2. 配置目录
    console.print("\n[bold]2️⃣  配置数据目录[/bold]")

    data_dir = Prompt.ask("数据目录", default=str(Path.home() / ".ai-toolkit" / "data"))
    models_dir = Prompt.ask("模型目录", default=str(Path.home() / ".ai-toolkit" / "models"))

    # 3. RAG 配置
    console.print("\n[bold]3️⃣  RAG 配置[/bold]")

    chunk_size = Prompt.ask("文本块大小", default="1000")
    chunk_overlap = Prompt.ask("文本块重叠", default="200")

    try:
        chunk_size = int(chunk_size)
        chunk_overlap = int(chunk_overlap)
    except ValueError:
        console.print("[red]无效的数字，使用默认值[/red]")
        chunk_size = 1000
        chunk_overlap = 200

    # 4. 创建配置
    console.print("\n[bold]4️⃣  创建配置[/bold]")

    config = Config(
        ollama_base_url=ollama_url,
        data_dir=Path(data_dir),
        models_dir=Path(models_dir),
        rag_chunk_size=chunk_size,
        rag_chunk_overlap=chunk_overlap,
    )

    # 创建目录
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.models_dir.mkdir(parents=True, exist_ok=True)
    config.prompts_dir.mkdir(parents=True, exist_ok=True)
    config.rag_dir.mkdir(parents=True, exist_ok=True)

    # 保存配置
    save_config(config)

    # 5. 显示配置摘要
    console.print("\n[bold green]✅ 配置完成![/bold green]\n")

    console.print(
        Panel(
            f"""[cyan]Ollama 地址:[/cyan] {config.ollama_base_url}
[cyan]数据目录:[/cyan] {config.data_dir}
[cyan]模型目录:[/cyan] {config.models_dir}
[cyan]Prompt目录:[/cyan] {config.prompts_dir}
[cyan]RAG目录:[/cyan] {config.rag_dir}
[cyan]Chunk大小:[/cyan] {config.rag_chunk_size}
[cyan]Chunk重叠:[/cyan] {config.rag_chunk_overlap}""",
            title="📋 配置摘要",
            border_style="cyan",
        )
    )

    # 6. 下一步提示
    console.print("\n[bold]🚀 下一步:[/bold]")
    console.print("1. 下载模型: [cyan]ai-toolkit models pull llama3.2[/cyan]")
    console.print("2. 查看状态: [cyan]ai-toolkit status[/cyan]")
    console.print("3. 查看帮助: [cyan]ai-toolkit --help[/cyan]")

    console.print("\n[green]开始使用 AI Toolkit 吧！[/green]\n")
