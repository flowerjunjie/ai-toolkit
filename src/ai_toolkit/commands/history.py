"""
历史记录管理
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime
import json

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="history")
def history_cli():
    """管理命令历史记录"""
    pass


@history_cli.command(name="list")
@click.option("--limit", "-n", type=int, default=20, help="显示条数")
@click.option("--command", "-c", help="过滤命令")
def list_history(limit: int, command: str):
    """显示历史记录"""
    config = get_config()
    history_file = config.data_dir / "history.json"

    if not history_file.exists():
        console.print("[yellow]暂无历史记录[/yellow]")
        return

    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    # 过滤
    if command:
        history = [h for h in history if command in h.get("command", "")]

    # 限制数量
    history = history[-limit:]

    if not history:
        console.print("[yellow]没有找到历史记录[/yellow]")
        return

    table = Table(title="📜 命令历史", show_header=True)
    table.add_column("时间", style="cyan")
    table.add_column("命令", style="green")
    table.add_column("参数", style="yellow")
    table.add_column("状态", style="blue")

    for entry in history:
        timestamp = entry.get("timestamp", "")
        cmd = entry.get("command", "")
        args = " ".join(entry.get("args", []))
        status = entry.get("status", "unknown")

        # 格式化时间
        try:
            dt = datetime.fromisoformat(timestamp)
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        table.add_row(timestamp, cmd, args[:50], status)

    console.print(table)
    console.print(f"\n共 {len(history)} 条记录")


@history_cli.command(name="clear")
@click.option("--force", "-f", is_flag=True, help="强制清空")
@click.option("--before", "-b", help="清空指定日期之前的记录")
def clear_history(force: bool, before: str):
    """清空历史记录"""
    config = get_config()
    history_file = config.data_dir / "history.json"

    if not history_file.exists():
        console.print("[yellow]暂无历史记录[/yellow]")
        return

    if not force:
        if not click.confirm("确定要清空历史记录吗？"):
            console.print("已取消")
            return

    if before:
        # 清空指定日期之前的记录
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)

        try:
            before_date = datetime.fromisoformat(before)
            new_history = [
                h for h in history
                if datetime.fromisoformat(h.get("timestamp", "")) >= before_date
            ]

            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(new_history, f, indent=2, ensure_ascii=False)

            console.print(f"✅ 已清空 {before} 之前的记录")
            console.print(f"   保留 {len(new_history)} 条记录")
        except Exception as e:
            console.print(f"[red]日期格式错误: {e}[/red]")
    else:
        # 清空所有
        history_file.unlink()
        console.print("✅ 历史记录已清空")


@history_cli.command(name="stats")
def history_stats():
    """显示历史统计"""
    config = get_config()
    history_file = config.data_dir / "history.json"

    if not history_file.exists():
        console.print("[yellow]暂无历史记录[/yellow]")
        return

    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    # 统计
    command_counts = {}
    status_counts = {}
    total = len(history)

    for entry in history:
        cmd = entry.get("command", "")
        status = entry.get("status", "unknown")

        command_counts[cmd] = command_counts.get(cmd, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    console.print(f"\n📊 历史统计 (共 {total} 条)\n")

    # 命令频率
    console.print("[bold]最常用命令:[/bold]")
    sorted_cmds = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for cmd, count in sorted_cmds:
        console.print(f"  {cmd}: {count} 次")

    console.print(f"\n[bold]状态分布:[/bold]")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        color = "green" if status == "success" else "red"
        console.print(f"  [{color}]{status}[/{color}]: {count} 次")


def add_history(command: str, args: list, status: str = "success"):
    """添加历史记录"""
    config = get_config()
    history_file = config.data_dir / "history.json"

    # 加载现有历史
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    # 添加新记录
    history.append({
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "args": args,
        "status": status,
    })

    # 限制历史记录数量（最多1000条）
    if len(history) > 1000:
        history = history[-1000:]

    # 保存
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
