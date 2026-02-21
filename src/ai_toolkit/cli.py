"""
AI Toolkit CLI - 主命令行接口
"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ai_toolkit.commands.alias import alias_cli
from ai_toolkit.commands.backup import backup_cli
from ai_toolkit.commands.batch import batch
from ai_toolkit.commands.benchmark import benchmark_cli
from ai_toolkit.commands.coding import coding_cli
from ai-toolkit.commands.config_cmd import config_cli
from ai_toolkit.commands.community import community_cli
from ai_toolkit.commands.content import content_cli
from ai_toolkit.commands.diag import diag_cli
from ai_toolkit.commands.export_cmd import export_cli
from ai_toolkit.commands.feedback import feedback_cli
from ai_toolkit.commands.guide import examples, quickstart
from ai_toolkit.commands.history import add_history, history_cli
from ai_toolkit.commands.init import init_command
from ai_toolkit.commands.market import market_cli
from ai_toolkit.commands.monitor import monitor_cli
from ai_toolkit.commands.models import models_cli
from ai_toolkit.commands.plugin import plugin_cli
from ai_toolkit.commands.prompts import prompts_cli
from ai_toolkit.commands.rag import rag_cli
from ai_toolkit.commands.rag_v2 import rag2_cli
from ai_toolkit.commands.revenue import revenue_cli
from ai_toolkit.commands.schedule_cmd import schedule_cli
from ai_toolkit.commands.seo import seo_cli
from ai_toolkit.commands.shell import shell
from ai_toolkit.commands.system_cmd import system_cli
from ai_toolkit.commands.template import template_cli
from ai_toolkit.commands.test import test
from ai_toolkit.commands.upgrade import upgrade_command
from ai_toolkit.commands.webui import webui

console = Console()


@click.group()
@click.version_option(version="0.3.0", prog_name="ai-toolkit")
@click.option("--verbose", "-v", is_flag=True, help="启用详细输出")
@click.option("--completion", is_flag=True, help="生成Bash自动补全脚本")
def main(verbose: bool = False, completion: bool = False):
    """
    🤖 AI Toolkit - 本地AI工具箱

    一个强大的本地AI模型管理和工具集，让AI开发更简单。

    官方文档: https://github.com/flowerjunjie/ai-toolkit

    快速开始:
    pip install ai-toolkit
    ai-toolkit init
    """
    if completion:
        completion_file = Path(__file__).parent / "utils" / "completion.sh"
        if completion_file.exists():
            print(completion_file.read_text())
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


# 添加所有子命令
main.add_command(models_cli)
main.add_command(prompts_cli)
main.add_command(rag_cli)
main.add_command(rag2_cli)
main.add_command(coding_cli)
main.add_command(benchmark_cli)
main.add_command(init_command)
main.add_command(upgrade_command)
main.add_command(alias_cli)
main.add_command(history_cli)
main.add_command(config_cli)
main.add_command(webui)
main.add_command(plugin_cli)
main.add_command(batch)
main.add_command(schedule_cli)
main.add_command(export_cli)
main.add_command(monitor_cli)
main.add_command(backup_cli)
main.add_command(system_cli)
main.add_command(diag_cli)
main.add_command(shell)
main.add_command(quickstart)
main.add_command(examples)
main.add_command(template_cli)
main.add_command(test)
main.add_command(market_cli)
main.add_command(revenue_cli)
main.add_command(community_cli)
main.add_command(feedback_cli)
main.add_command(content_cli)
main.add_command(seo_cli)


if __name__ == "__main__":
    main()
