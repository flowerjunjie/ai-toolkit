"""
AI Toolkit CLI - 主命令行接口
"""

import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

from ai_toolkit.commands.models import models_cli
from ai_toolkit.commands.prompts import prompts_cli
from ai_toolkit.commands.rag import rag_cli
from ai_toolkit.commands.rag_v2 import rag2_cli
from ai_toolkit.commands.benchmark import benchmark_cli
from ai_toolkit.commands.init import init_command
from ai_toolkit.commands.upgrade import upgrade_command
from ai_toolkit.commands.coding import coding_cli
from ai_toolkit.commands.alias import alias_cli
from ai_toolkit.commands.history import history_cli, add_history
from ai_toolkit.commands.config_cmd import config_cli
from ai_toolkit.commands.webui import webui
from ai_toolkit.commands.plugin import plugin_cli
from ai_toolkit.commands.batch import batch
from ai_toolkit.commands.schedule_cmd import schedule_cli

console = Console()


@click.group()
@click.version_option(version="0.3.0", prog_name="ai-toolkit")
@click.option("--verbose", "-v", is_flag=True, help="启用详细输出")
@click.option("--completion", is_flag=True, help="生成Bash自动补全脚本")
def main(verbose: bool = False, completion: bool = False):
    """
    🤖 AI Toolkit - 本地AI工具箱

    一个强大的本地AI模型管理和工具集，让AI开发更简单。
    """
    if completion:
        from ai_toolkit.utils.completion import _ai_toolkit_completion
        import inspect
        source = inspect.getsource(_ai_toolkit_completion)
        print(source)
        return

    if verbose:
        console.print("[dim]调试模式已启用[/dim]")


@main.command()
def status():
    """显示系统状态"""
    from ai_toolkit.core.config import get_config

    config = get_config()

    table = Table(title="🤖 AI Toolkit 状态", show_header=True, header_style="bold magenta")
    table.add_column("项目", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("说明")

    table.add_row("版本", "0.3.0", "生产就绪")
    table.add_row("配置文件", str(config.config_path), "配置文件路径")
    table.add_row("数据目录", str(config.data_dir), "数据存储目录")
    table.add_row("模型目录", str(config.models_dir), "本地模型存储")

    console.print(table)


# 添加子命令组
main.add_command(models_cli)
main.add_command(prompts_cli)
main.add_command(rag_cli)
main.add_command(rag2_cli)  # 向量检索RAG
main.add_command(coding_cli)  # AI编码助手
main.add_command(benchmark_cli)
main.add_command(init_command)
main.add_command(upgrade_command)
main.add_command(alias_cli)  # 命令别名
main.add_command(history_cli)  # 历史记录
main.add_command(config_cli)  # 配置管理
main.add_command(webui)  # Web UI
main.add_command(plugin_cli)  # 插件系统
main.add_command(batch)  # 批处理
main.add_command(schedule_cli)  # 任务调度


if __name__ == "__main__":
    main()
