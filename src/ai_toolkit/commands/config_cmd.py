"""
配置导入导出
"""

import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from ai_toolkit.core.config import Config, get_config, load_config, save_config

console = Console()


@click.group(name="config")
def config_cli():
    """管理配置"""
    pass


@config_cli.command(name="export")
@click.argument("output_file", type=click.Path())
@click.option("--include-api-keys", is_flag=True, help="包含API密钥")
def export_config(output_file: str, include_api_keys: bool):
    """导出配置到文件"""
    config = get_config()

    # 导出配置
    export_data = {
        "ollama_base_url": config.ollama_base_url,
        "ollama_timeout": config.ollama_timeout,
        "rag_chunk_size": config.rag_chunk_size,
        "rag_chunk_overlap": config.rag_chunk_overlap,
        "rag_top_k": config.rag_top_k,
        "data_dir": str(config.data_dir),
        "models_dir": str(config.models_dir),
        "prompts_dir": str(config.prompts_dir),
        "rag_dir": str(config.rag_dir),
    }

    # 可选：包含API密钥
    if include_api_keys:
        from ai_toolkit.core.api_manager import get_api_manager

        api_manager = get_api_manager()
        export_data["api_keys"] = [
            {
                "provider": key.provider,
                "model": key.model,
                "base_url": key.base_url,
                # 不导出实际的API密钥
                "api_key": "***HIDDEN***",
            }
            for key in api_manager.api_keys
        ]

    # 保存
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    console.print(f"✅ 配置已导出到: {output_path}")

    if include_api_keys:
        console.print("[dim]注: API密钥已隐藏，未导出实际值[/dim]")


@config_cli.command(name="import")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--merge", is_flag=True, help="合并配置而不是覆盖")
def import_config(input_file: str, merge: bool):
    """从文件导入配置"""
    input_path = Path(input_file)

    with open(input_path, "r", encoding="utf-8") as f:
        import_data = json.load(f)

    console.print(f"📥 导入配置: {input_path}\n")

    if merge:
        # 合并配置
        current_config = get_config()
        config = Config(**{**current_config.model_dump(), **import_data})
    else:
        # 完全替换
        config = Config(**import_data)

    # 保存配置
    save_config(config)

    console.print("✅ 配置已导入")
    console.print("\n导入的配置:")
    console.print(
        Panel(
            f"""[cyan]Ollama地址:[/cyan] {config.ollama_base_url}
[cyan]超时:[/cyan] {config.ollama_timeout}s
[cyan]Chunk大小:[/cyan] {config.rag_chunk_size}
[cyan]数据目录:[/cyan] {config.data_dir}""",
            title="📋 配置",
            border_style="cyan",
        )
    )


@config_cli.command(name="show")
def show_config():
    """显示当前配置"""
    config = get_config()

    console.print(
        Panel(
            f"""[cyan]Ollama地址:[/cyan] {config.ollama_base_url}
[cyan]超时:[/cyan] {config.ollama_timeout}s
[cyan]RAG配置:[/cyan]
  - Chunk大小: {config.rag_chunk_size}
  - 重叠: {config.rag_chunk_overlap}
  - Top-K: {config.rag_top_k}
[cyan]目录:[/cyan]
  - 数据: {config.data_dir}
  - 模型: {config.models_dir}
  - Prompts: {config.prompts_dir}
  - RAG: {config.rag_dir}""",
            title="📋 当前配置",
            border_style="cyan",
        )
    )


@config_cli.command(name="reset")
@click.option("--force", "-f", is_flag=True, help="强制重置")
def reset_config(force: bool):
    """重置为默认配置"""
    if not force:
        if not click.confirm("确定要重置配置吗？这将删除所有自定义配置"):
            console.print("已取消")
            return

    from ai_toolkit.core.config import initialize_config

    config = initialize_config()

    console.print("✅ 配置已重置为默认值")
    console.print(f"📁 数据目录: {config.data_dir}")
