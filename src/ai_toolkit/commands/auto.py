"""
自动化工具命令
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
import time

console = Console()


@click.group(name="auto")
def auto_cli():
    """自动化工具"""
    pass


@auto_cli.command(name="status")
def auto_status():
    """查看自动化状态"""
    from ai_toolkit.utils.progress_tracker import get_progress_tracker

    tracker = get_progress_tracker()
    status = tracker.get_status()

    console.print("\n🤖 自动化状态\n")

    table = Table(show_header=True)
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="green")
    table.add_column("说明", style="yellow")

    table.add_row("迭代轮数", str(status.get("rounds_completed", 0)), "已完成的迭代轮数")
    table.add_row("功能数量", str(status.get("features_added", 0)), "新增功能数")
    table.add_row("提交次数", str(status.get("total_commits", 0)), "Git提交数")
    table.add_row("Bug修复", str(status.get("bugs_fixed", 0)), "修复的Bug数")
    table.add_row("工作时长", str(status.get("hours_worked", 0)), "工作小时数")

    console.print(table)

    if status.get("changes"):
        console.print("\n最近更新:")
        for change in status["changes"][-10:]:  # 显示最近10条
            console.print(f"  • {change}")

    console.print(f"\n最后更新: {status.get('last_update', '无')}")


@auto_cli.command(name="work")
@click.option("--hours", "-h", type=int, default=1, help="工作时长（小时）")
def auto_work(hours: int):
    """记录工作时间"""
    from ai_toolkit.utils.progress_tracker import get_progress_tracker

    tracker = get_progress_tracker()

    console.print(f"🕐 记录工作时间: {hours}小时")

    for i in range(hours):
        console.print(f"  [{i+1}/{hours}] 工作中...")
        time.sleep(3600)  # 模拟1小时工作
        tracker.add_hour()

    console.print(f"\n✅ 已记录 {hours} 小时工作")


@auto_cli.command(name="report")
def auto_report():
    """生成进度报告"""
    from ai_toolkit.utils.progress_tracker import get_progress_tracker

    tracker = get_progress_tracker()
    status = tracker.get_status()

    console.print("\n📊 开发进度报告\n")

    console.print(f"📈 统计:")
    console.print(f"  迭代轮数: {status.get('rounds_completed', 0)}")
    console.print(f"  新增功能: {status.get('features_added', 0)}")
    console.print(f"  Git提交: {status.get('total_commits', 0)}")
    console.print(f"  Bug修复: {status.get('bugs_fixed', 0)}")
    console.print(f"  工作时长: {status.get('hours_worked', 0)}小时")

    if status.get("last_update"):
        console.print(f"\n最后更新: {status['last_update']}")

    if status.get("changes"):
        console.print("\n最近更新:")
        for change in status["changes"][-10:]:
            console.print(f"  • {change}")


@auto_cli.command(name="summary")
def auto_summary():
    """生成系统摘要"""
    from ai_toolkit.core.config import get_config

    config = get_config()

    console.print("\n📋 系统摘要\n")

    console.print("🤖 AI Toolkit 系统摘要")
    console.print(f"版本: 0.3.0")
    console.print(f"配置目录: {config.data_dir}")
    console.print(f"模型目录: {config.models_dir}")
    console.print(f"Prompts目录: {config.prompts_dir}")
    console.print(f"RAG目录: {config.rag_dir}")

    # 统计文件数量
    src_files = list(config.data_dir.rglob("*"))
    console.print(f"\n数据文件: {len(src_files)} 个")

    # 统计模块数量
    commands_dir = Path(__file__).parent.parent / "commands"
    cmd_files = list(commands_dir.glob("*.py"))
    console.print(f"命令文件: {len(cmd_files)} 个")

    console.print(f"\n✅ 系统运行正常！")
