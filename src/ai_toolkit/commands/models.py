"""
模型管理命令
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
from pathlib import Path

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="models")
def models_cli():
    """管理本地AI模型"""
    pass


@models_cli.command(name="list")
def list_models():
    """列出已安装的模型"""
    config = get_config()

    try:
        # 从Ollama获取模型列表
        response = requests.get(f"{config.ollama_base_url}/api/tags", timeout=config.ollama_timeout)
        response.raise_for_status()
        data = response.json()

        models = data.get("models", [])

        if not models:
            console.print("[yellow]未找到已安装的模型[/yellow]")
            console.print("提示: 使用 [cyan]ai-toolkit models pull <model-name>[/cyan] 下载模型")
            return

        table = Table(title="📦 已安装的模型", show_header=True)
        table.add_column("模型名称", style="cyan")
        table.add_column("大小", style="green")
        table.add_column("修改时间", style="yellow")

        for model in models:
            name = model.get("name", "unknown")
            size = model.get("size", 0)
            size_gb = size / (1024**3) if size else 0
            modified = model.get("modified_at", "unknown")[:10]

            table.add_row(name, f"{size_gb:.2f} GB", modified)

        console.print(table)
        console.print(f"\n共 {len(models)} 个模型")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]错误: 无法连接到Ollama服务[/red]")
        console.print(f"[dim]请确保Ollama正在运行: {config.ollama_base_url}[/dim]")
        console.print(f"[dim]安装Ollama: https://ollama.ai[/dim]")


@models_cli.command(name="pull")
@click.argument("model_name")
def pull_model(model_name: str):
    """下载一个模型"""
    config = get_config()

    console.print(f"📥 正在下载模型: [cyan]{model_name}[/cyan]")
    console.print("[dim]这可能需要几分钟...[/dim]")

    try:
        # 使用Ollama API下载模型
        response = requests.post(
            f"{config.ollama_base_url}/api/pull",
            json={"name": model_name},
            timeout=config.ollama_timeout * 10,
            stream=True,
        )

        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                # 显示进度
                console.print(f"[dim]📦 {data}[/dim]", end="\r")

        console.print(f"\n✅ 模型 [cyan]{model_name}[/cyan] 下载完成!")

    except requests.exceptions.RequestException as e:
        console.print(f"\n[red]下载失败: {e}[/red]")


@models_cli.command(name="run")
@click.argument("model_name")
@click.argument("prompt")
@click.option("--temperature", "-t", type=float, default=0.7, help="温度参数 (0-1)")
@click.option("--max-tokens", type=int, default=500, help="最大生成token数")
def run_model(model_name: str, prompt: str, temperature: float, max_tokens: int):
    """运行模型生成文本"""
    config = get_config()

    console.print(f"🤖 运行模型: [cyan]{model_name}[/cyan]")
    console.print(f"💬 Prompt: [dim]{prompt[:100]}...[/dim]\n")

    try:
        response = requests.post(
            f"{config.ollama_base_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            },
            timeout=config.ollama_timeout * 2,
            stream=True,
        )

        console.print("[bold]回复:[/bold]")
        console.print()

        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                import json

                try:
                    json_data = json.loads(data)
                    if "response" in json_data:
                        console.print(json_data["response"], end="")
                    if json_data.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

        console.print("\n")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]运行失败: {e}[/red]")


@models_cli.command(name="delete")
@click.argument("model_name")
@click.option("--force", "-f", is_flag=True, help="强制删除，不确认")
def delete_model(model_name: str, force: bool):
    """删除一个模型"""
    if not force:
        console.print(f"⚠️  即将删除模型: [red]{model_name}[/red]")
        if not click.confirm("确定要删除吗？"):
            console.print("已取消")
            return

    config = get_config()

    try:
        response = requests.delete(
            f"{config.ollama_base_url}/api/delete",
            json={"name": model_name},
            timeout=config.ollama_timeout,
        )
        response.raise_for_status()

        console.print(f"✅ 模型 [cyan]{model_name}[/cyan] 已删除")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]删除失败: {e}[/red]")


@models_cli.command(name="info")
@click.argument("model_name")
def model_info(model_name: str):
    """显示模型详细信息"""
    config = get_config()

    try:
        # 获取模型信息
        response = requests.get(f"{config.ollama_base_url}/api/tags", timeout=config.ollama_timeout)
        response.raise_for_status()
        data = response.json()

        models = data.get("models", [])
        model = next((m for m in models if m.get("name") == model_name), None)

        if not model:
            console.print(f"[red]未找到模型: {model_name}[/red]")
            return

        size = model.get("size", 0)
        size_gb = size / (1024**3) if size else 0
        modified = model.get("modified_at", "unknown")

        info_panel = Panel(
            f"""[cyan]模型名称:[/cyan] {model.get('name')}
[cyan]大小:[/cyan] {size_gb:.2f} GB
[cyan]修改时间:[/cyan] {modified}
[cyan]摘要:[/cyan] {model.get('digest', 'N/A')[:16]}...""",
            title=f"📦 {model_name}",
            border_style="cyan",
        )

        console.print(info_panel)

    except requests.exceptions.RequestException as e:
        console.print(f"[red]获取信息失败: {e}[/red]")
