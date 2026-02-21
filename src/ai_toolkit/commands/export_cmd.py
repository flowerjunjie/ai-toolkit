"""
数据导出命令
"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime

from ai_toolkit.core.config import get_config
from ai_toolkit.core.api_manager import get_api_manager

console = Console()


@click.group(name="export")
def export_cli():
    """导出数据"""
    pass


@export_cli.command(name="prompts")
@click.option("--output", "-o", type=click.Path(), help="输出文件")
def export_prompts(output: str):
    """导出所有Prompt模板"""
    config = get_config()
    prompts_dir = config.prompts_dir

    if not prompts_dir.exists():
        console.print("[yellow]暂无Prompt模板[/yellow]")
        return

    prompts = []
    for prompt_file in prompts_dir.glob("*.json"):
        with open(prompt_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            prompts.append(data)

    if output:
        output_path = Path(output)
    else:
        output_path = Path.cwd() / f"prompts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    console.print(f"✅ 已导出 {len(prompts)} 个Prompt模板")
    console.print(f"   文件: {output_path}")


@export_cli.command(name="rag")
@click.argument("name")
@click.option("--output", "-o", type=click.Path(), help="输出文件")
@click.option("--format", "-f", default="json", type=click.Choice(["json", "txt", "md"]), help="导出格式")
def export_rag(name: str, output: str, format: str):
    """导出RAG知识库"""
    config = get_config()

    if format == "json":
        metadata_file = config.rag_dir / name / "metadata.json"
    else:
        metadata_file = config.rag_dir / name / "metadata.json"

    if not metadata_file.exists():
        console.print(f"[red]知识库不存在: {name}[/red]")
        return

    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if output:
        output_path = Path(output)
    else:
        output_path = Path.cwd() / f"rag_{name}_export.{format}"

    if format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif format == "txt":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"知识库名称: {data['name']}\n")
            f.write(f"文档路径: {data['docs_path']}\n")
            f.write(f"文档数量: {data.get('num_documents', 'N/A')}\n")
            f.write(f"文本块数: {data.get('num_chunks', 'N/A')}\n")
    elif format == "md":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {data['name']}\n\n")
            f.write(f"- **路径**: {data['docs_path']}\n")
            f.write(f"- **文档数**: {data.get('num_documents', 'N/A')}\n")
            f.write(f"- **文本块数**: {data.get('num_chunks', 'N/A')}\n")
            f.write(f"- **Chunk大小**: {data.get('chunk_size', 'N/A')}\n")

    console.print(f"✅ 知识库已导出: {output_path}")


@export_cli.command(name="stats")
def export_stats():
    """导出使用统计"""
    api_manager = get_api_manager()

    stats = {
        "timestamp": datetime.now().isoformat(),
        "api_keys": api_manager.get_status(),
        "total_keys": api_manager.get_total_count(),
        "available_keys": api_manager.get_available_count(),
    }

    output_path = Path.cwd() / f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    console.print(f"✅ 统计已导出: {output_path}")


@export_cli.command(name="all")
@click.option("--output-dir", "-d", type=click.Path(), help="输出目录")
def export_all(output_dir: str):
    """导出所有数据"""
    if not output_dir:
        output_dir = Path.cwd() / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"📦 导出所有数据到: {output_dir}\n")

    # 导出Prompts
    from ai_toolkit.commands.export_cmd import export_prompts as export_prompts_func

    ctx = click.Context(export_prompts_func)
    ctx.params = {"output": str(output_dir / "prompts.json")}
    export_prompts_func(ctx)

    # 导出统计
    ctx = click.Context(export_stats)
    export_stats(ctx)

    console.print(f"\n✅ 所有数据已导出到: {output_dir}")
