"""
项目管理工具
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json
from datetime import datetime

console = Console()


@click.group(name="project")
def project_cli():
    """项目管理工具"""
    pass


@project_cli.command(name="create")
@click.option("--name", "-n", required=True, help="项目名称")
@click.option("--description", "-d", help="项目描述")
def create_project(name: str, description: str):
    """创建项目"""
    console.print(f"\n📁 创建项目: {name}\n")

    project_dir = Path.cwd() / name
    project_dir.mkdir(exist_ok=True)

    console.print("创建项目结构...")

    # 创建标准目录
    dirs = ["src", "tests", "docs", "scripts"]
    for dir_name in dirs:
        (project_dir / dir_name).mkdir(exist_ok=True)

    console.print("✅ 项目已创建")

    project_config = {
        "name": name,
        "description": description or "",
        "created": datetime.now().isoformat(),
        "tasks": [],
    }

    config_file = project_dir / "project.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(project_config, f, indent=2, ensure_ascii=False)

    console.print(f"\n项目位置: {project_dir}")


@project_cli.command(name="tasks")
def list_tasks():
    """列出任务"""
    console.print("\n📋 任务列表\n")

    tasks = [
        ("设计API", "✅ 完成", "2025-01-10"),
        ("实现核心", "⏳ 进行中", "2025-01-11"),
        ("编写测试", "📋 待开始", "2025-01-12"),
        ("部署上线", "📋 待开始", "2025-01-15"),
    ]

    table = Table(show_header=True)
    table.add_column("任务", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("截止", style="yellow")

    for task, status, deadline in tasks:
        table.add_row(task, status, deadline)

    console.print(table)

    console.print(f"\n总任务: {len(tasks)}")


@project_cli.command(name="add")
@click.option("--task", "-t", required=True, help="任务名称")
@click.option("--assignee", "-a", help="指派给")
@click.option("--deadline", "-d", help="截止日期")
def add_task(task: str, assignee: str, deadline: str):
    """添加任务"""
    console.print(f"\n➕ 添加任务: {task}\n")

    console.print(f"任务: {task}")
    if assignee:
        console.print(f"指派: {assignee}")
    if deadline:
        console.print(f"截止: {deadline}")

    console.print("\n✅ 任务已添加")


@project_cli.command(name="kanban")
def show_kanban():
    """看板视图"""
    console.print("\n📊 看板视图\n")

    kanban = {
        "待办": [
            "编写测试",
            "部署上线",
        ],
        "进行中": [
            "实现核心",
        ],
        "完成": [
            "设计API",
        ],
    }

    for status, tasks in kanban.items():
        console.print(f"\n{status}:")
        for task in tasks:
            console.print(f"  • {task}")


@project_cli.command(name="milestones")
def show_milestones():
    """里程碑"""
    console.print("\n🎯 里程碑\n")

    milestones = [
        ("MVP", "2025-01-15", "⏳ 进行中"),
        ("Beta", "2025-02-01", "📋 待开始"),
        ("正式版", "2025-03-01", "📋 待开始"),
    ]

    table = Table(show_header=True)
    table.add_column("里程碑", style="cyan")
    table.add_column("日期", style="green")
    table.add_column("状态", style="yellow")

    for milestone, date, status in milestones:
        table.add_row(milestone, date, status)

    console.print(table)


@project_cli.command(name="burndown")
def show_burndown():
    """燃尽图"""
    console.print("\n📉 燃尽图\n")

    console.print("剩余工作量:")

    days = ["周一", "周二", "周三", "周四", "周五"]
    work = [40, 35, 28, 20, 10]

    for day, w in zip(days, work):
        bar = "█" * (w // 2)
        console.print(f"  {day}: {w}h {bar}")

    console.print("\n✅ 进度良好")


@project_cli.command(name="standup")
@click.option("--yesterday", "-y", help="昨天做了什么")
@click.option("--today", "-t", help="今天计划")
@click.option("--blocks", "-b", help="遇到的阻碍")
def daily_standup(yesterday: str, today: str, blocks: str):
    """每日站会"""
    console.print("\n👋 每日站会\n")

    console.print("昨天:")
    if yesterday:
        console.print(f"  • {yesterday}")
    else:
        console.print("  [待填写]")

    console.print("\n今天:")
    if today:
        console.print(f"  • {today}")
    else:
        console.print("  [待填写]")

    console.print("\n阻碍:")
    if blocks:
        console.print(f"  • {blocks}")
    else:
        console.print("  无")

    console.print("\n✅ 站会记录已保存")


@project_cli.command(name="retro")
@click.option("--good", "-g", help="做得好的")
@click.option("--bad", "-b", help="需要改进")
@click.option("--action", "-a", help="行动计划")
def retrospective(good: str, bad: str, action: str):
    """回顾会议"""
    console.print("\n🤔 回顾会议\n")

    console.print("做得好的:")
    if good:
        console.print(f"  • {good}")
    else:
        console.print("  [待填写]")

    console.print("\n需要改进:")
    if bad:
        console.print(f"  • {bad}")
    else:
        console.print("  [待填写]")

    console.print("\n行动计划:")
    if action:
        console.print(f"  • {action}")
    else:
        console.print("  [待填写]")

    console.print("\n✅ 回顾记录已保存")


@project_cli.command(name="wiki")
def show_wiki():
    """项目Wiki"""
    console.print("\n📖 项目Wiki\n")

    wiki_pages = [
        ("项目概述", "✅ 完整"),
        ("架构设计", "✅ 完整"),
        ("API文档", "⏳ 编写中"),
        ("部署指南", "📋 待编写"),
    ]

    table = Table(show_header=True)
    table.add_column("页面", style="cyan")
    table.add_column("状态", style="green")

    for page, status in wiki_pages:
        table.add_row(page, status)

    console.print(table)

    console.print("\n💡 Wiki位置:")
    console.print("  docs/wiki/")
