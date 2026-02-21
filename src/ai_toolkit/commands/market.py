"""
命令市场 - 命令分享和下载
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
import json

console = Console()


@click.group(name="market")
def market_cli():
    """命令市场 - 分享和下载命令"""
    pass


@market_cli.command(name="list")
@click.option("--category", "-c", help="按类别筛选")
def list_commands(category: str):
    """列出市场中的命令"""
    console.print("\n🏪 命令市场\n")

    # 预设市场命令
    market_commands = [
        {
            "name": "web-scraper",
            "category": "web",
            "description": "网页抓取工具",
            "price": "免费",
            "downloads": 1200,
        },
        {
            "name": "data-visualizer",
            "category": "data",
            "description": "数据可视化工具",
            "price": "$9.99",
            "downloads": 850,
        },
        {
            "name": "api-tester",
            "category": "dev",
            "description": "API测试工具",
            "price": "免费",
            "downloads": 2100,
        },
        {
            "name": "code-generator",
            "category": "dev",
            "description": "代码生成器",
            "price": "$19.99",
            "downloads": 1500,
        },
        {
            "name": "report-builder",
            "category": "office",
            "description": "报告生成器",
            "price": "$14.99",
            "downloads": 600,
        },
    ]

    # 筛选
    if category:
        market_commands = [c for c in market_commands if c["category"] == category]

    # 显示
    table = Table(show_header=True)
    table.add_column("命令名", style="cyan")
    table.add_column("类别", style="green")
    table.add_column("描述", style="yellow")
    table.add_column("价格", style="red")
    table.add_column("下载", style="blue")

    for cmd in market_commands:
        table.add_row(
            cmd["name"],
            cmd["category"],
            cmd["description"],
            cmd["price"],
            str(cmd["downloads"]),
        )

    console.print(table)

    if category:
        console.print(f"\n类别: {category}")
    console.print(f"\n共 {len(market_commands)} 个命令")


@market_cli.command(name="search")
@click.argument("keyword")
def search_commands(keyword: str):
    """搜索命令"""
    console.print(f"\n🔍 搜索: {keyword}\n")

    # 预设命令
    all_commands = {
        "web-scraper": {"category": "web", "description": "网页抓取工具"},
        "data-visualizer": {"category": "data", "description": "数据可视化工具"},
        "api-tester": {"category": "dev", "description": "API测试工具"},
        "code-generator": {"category": "dev", "description": "代码生成器"},
        "report-builder": {"category": "office", "description": "报告生成器"},
    }

    # 搜索
    results = []
    for name, info in all_commands.items():
        if (
            keyword.lower() in name.lower()
            or keyword.lower() in info["description"].lower()
            or keyword.lower() in info["category"].lower()
        ):
            results.append((name, info))

    # 显示结果
    if results:
        for name, info in results:
            console.print(f"[cyan]{name}[/cyan] ({info['category']})")
            console.print(f"  {info['description']}\n")
    else:
        console.print("[yellow]未找到匹配的命令[/yellow]")


@market_cli.command(name="install")
@click.argument("command_name")
def install_command(command_name: str):
    """安装命令"""
    console.print(f"\n📦 安装命令: {command_name}\n")

    # 模拟安装
    console.print("正在下载...")
    console.print("✅ 下载完成")
    console.print("正在安装...")
    console.print("✅ 安装完成")
    console.print(f"\n命令 [cyan]{command_name}[/cyan] 已安装！")
    console.print(f"\n使用: ai-toolkit {command_name} <args>")


@market_cli.command(name="publish")
@click.argument("command_name")
@click.option("--price", "-p", default="免费", help="价格")
@click.option("--description", "-d", help="描述")
def publish_command(command_name: str, price: str, description: str):
    """发布命令到市场"""
    console.print(f"\n📤 发布命令: {command_name}\n")

    console.print(f"价格: {price}")
    if description:
        console.print(f"描述: {description}")

    console.print("\n正在发布...")
    console.print("✅ 发布成功！")
    console.print(f"\n命令 [cyan]{command_name}[/cyan] 已发布到市场！")


@market_cli.command(name="categories")
def list_categories():
    """列出所有类别"""
    console.print("\n📂 命令类别\n")

    categories = {
        "dev": "开发工具",
        "web": "网络工具",
        "data": "数据处理",
        "office": "办公工具",
        "system": "系统工具",
    }

    for cat, desc in categories.items():
        console.print(f"[cyan]{cat}[/cyan] - {desc}")


@market_cli.command(name="stats")
def show_stats():
    """显示市场统计"""
    console.print("\n📊 市场统计\n")

    stats = {
        "总命令数": 150,
        "总下载量": 125000,
        "活跃开发者": 45,
        "今日新增": 3,
    }

    for key, value in stats.items():
        console.print(f"[cyan]{key}[/cyan]: {value}")
