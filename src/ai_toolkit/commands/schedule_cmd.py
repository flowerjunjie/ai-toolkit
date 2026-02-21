"""
任务调度命令
"""

import click
from rich.console import Console
from rich.table import Table
import time

from ai_toolkit.core.scheduler import get_scheduler, TaskScheduler

console = Console()


@click.group(name="schedule")
def schedule_cli():
    """管理定时任务"""
    pass


@schedule_cli.command(name="list")
def list_tasks():
    """列出所有定时任务"""
    scheduler = get_scheduler()

    tasks = scheduler.list_tasks()

    if not tasks:
        console.print("[yellow]暂无定时任务[/yellow]")
        console.print("使用 [cyan]ai-toolkit schedule add[/cyan] 添加任务")
        return

    table = Table(title="⏰ 定时任务", show_header=True)
    table.add_column("任务名称", style="cyan")
    table.add_column("调度", style="green")

    for name, job_type in tasks.items():
        table.add_row(name, job_type)

    console.print(table)
    console.print(f"\n共 {len(tasks)} 个任务")


@schedule_cli.command(name="add")
@click.argument("name")
@click.argument("interval", type=int)
@click.argument("command")
@click.option("--unit", "-u", default="minutes", help="时间单位 (seconds/minutes/hours/days)")
def add_task(name: str, interval: int, command: str, unit: str):
    """添加定时任务"""
    scheduler = get_scheduler()

    def task_func():
        import subprocess
        subprocess.run(command, shell=True)

    scheduler.add_task(name, task_func, interval, unit)

    console.print(f"✅ 任务已添加: {name}")
    console.print(f"   间隔: {interval} {unit}")
    console.print(f"   命令: {command}")


@schedule_cli.command(name="remove")
@click.argument("name")
def remove_task(name: str):
    """移除定时任务"""
    scheduler = get_scheduler()

    scheduler.remove_task(name)

    console.print(f"✅ 任务已移除: {name}")


@schedule_cli.command(name="start")
@click.option("--daemon", "-d", is_flag=True, help="后台运行")
def start_scheduler(daemon: bool):
    """启动调度器"""
    scheduler = get_scheduler()

    if daemon:
        scheduler.start()
        console.print("✅ 调度器已在后台启动")
        console.print(f"\n使用 [cyan]ai-toolkit schedule list[/cyan] 查看任务")
        console.print("使用 [cyan]ai-toolkit schedule stop[/cyan] 停止调度器")
    else:
        console.print("调度器运行中... (按 Ctrl+C 停止)")
        console.print("")

        try:
            scheduler.run_scheduler()
        except KeyboardInterrupt:
            console.print("\n[yellow]调度器已停止[/yellow]")


@schedule_cli.command(name="stop")
def stop_scheduler():
    """停止调度器"""
    scheduler = get_scheduler()

    scheduler.stop()

    console.print("✅ 调度器已停止")


@schedule_cli.command(name="run")
def run_once():
    """运行一次待执行的任务"""
    scheduler = get_scheduler()

    scheduler.run_once()

    console.print("✅ 已执行待执行的任务")
