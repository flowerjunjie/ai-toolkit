"""
定期报告生成器
"""

import click
from pathlib import Path
from rich.console import Console
from datetime import datetime, timedelta
from typing import Dict, List, Any

console = Console()


@click.command()
@click.option("--period", "-p", default="daily", type=click.Choice(["daily", "weekly", "monthly", "all"])
@click.option("--output", "-o", type=click.Path(), help="输出文件")
def report(period: str, output: str):
    """生成报告"""
    from ai_toolkit.core.config import get_config
    from ai_toolkit.utils.progress_tracker import get_progress_tracker

    tracker = get_progress_tracker()
    config = get_config()

    console.print("\n📊 生成报告\n")

    # 收集数据
    status = tracker.get_status()

    # 生成报告内容
    report_lines = []
    report_lines.append("# AI Toolkit 开发进度报告")
    report_lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"报告周期: {period}")
    report_lines.append("\n## 📊 开发统计")
    report_lines.append(f"- 迭代轮数: {status.get('rounds_completed', 0)}")
    report_lines.append(f"- 新增功能: {status.get('features_added', 0)}")
    report_lines.append(f"- Git提交: {status.get('total_commits', 0)}")
    report_lines.append(f"- Bug修复: {status.get('bugs_fixed', 0)}")
    report_lines.append(f"- 工作时长: {status.get('hours_worked} 小时}")
    report_lines.append("\n## 🎯 当前进度")
    report_lines.append(f"- 版本: v0.3.0")
    report_lines.append(f"- 功能模块: 21个")
    report_lines.append(f"- 命令数量: 75+")
    report_lines.append(f"- 代码行数: 13000+")

    if status.get("changes"):
        report_lines.append("\n## 📝 最近更新")
        for i, change in status["changes"][-10:]:
            report_lines.append(f"- {change}")

    report_text = "\n".join(report_lines)

    # 输出报告
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        console.print(f"✅ 报告已生成: {output_path}")
    else:
        console.print(report_text)


@click.command()
@click.option("--days", "-d", default=7, help="统计天数")
def stats(days: int):
    """显示统计信息"""
    import subprocess

    console.print(f"\n📊 最近 {days} 天的统计\n")

    # Git提交统计
    result = subprocess.run(
        ["git", "log", "--since", f"{days} days ago", "--oneline"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
    )

    commits = result.stdout.strip().split("\n") if result.stdout.strip() else []

    if commits:
        console.print(f"📝 Git提交: {len(commits)} 次")

        # 按作者统计
        authors = {}
        for commit in commits:
            author = commit.split(" ")[1] if " " in commit else "Unknown"
            authors[author] = authors.get(author, 0) + 1

        console.print(f"\n贡献者:")
        for author, count in sorted(authors.items(), key=lambda x: -x[1]):
            console.print(f"  • {author}: {count} commits")
    else:
        console.print("最近无提交记录")


@click.command()
@click.option("--limit", "-n", default=20, help="显示条数")
def show_log(limit: int):
    """显示最近的Git日志"""
    import subprocess

    result = subprocess.run(
        ["git", "log", "--oneline", f"-{limit}"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
    )

    console.print(f"\n📝 最近 {limit} 条提交:\n")

    if result.stdout:
        console.print(result.stdout)
    else:
        console.print("暂无提交记录")
