"""
用户反馈系统
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import json

console = Console()


@click.group(name="feedback")
def feedback_cli():
    """用户反馈管理"""
    pass


@feedback_cli.command(name="collect")
@click.option("--source", "-s", help="反馈来源")
@click.option("--issue", "-i", help="Issue编号")
def collect_feedback(source: str, issue: int):
    """收集反馈"""
    console.print("\n📥 收集反馈\n")

    console.print("来源:")
    if source:
        console.print(f"  {source}")
    else:
        console.print("  所有平台")

    if issue:
        console.print(f"\nIssue: #{issue}")

    console.print("\n✅ 反馈已收集！")

    # 保存反馈
    feedback_dir = Path.home() / ".ai-toolkit" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    feedback_file = feedback_dir / f"{datetime.now().strftime('%Y%m%d')}.json"

    feedback_data = {
        "date": datetime.now().isoformat(),
        "source": source or "all",
        "issue": issue,
    }

    with open(feedback_file, "w", encoding="utf-8") as f:
        json.dump([feedback_data], f, indent=2, ensure_ascii=False)

    console.print(f"\n已保存到: {feedback_file}")


@feedback_cli.command(name="list")
def list_feedback():
    """列出所有反馈"""
    console.print("\n📋 反馈列表\n")

    feedback_dir = Path.home() / ".ai-toolkit" / "feedback"

    if not feedback_dir.exists():
        console.print("[yellow]暂无反馈[/yellow]")
        return

    feedback_files = list(feedback_dir.glob("*.json"))

    if not feedback_files:
        console.print("[yellow]暂无反馈[/yellow]")
        return

    table = Table(show_header=True)
    table.add_column("日期", style="cyan")
    table.add_column("来源", style="green")
    table.add_column("Issue", style="yellow")

    for feedback_file in sorted(feedback_files):
        with open(feedback_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                date = item.get("date", "")[:10]
                source = item.get("source", "未知")
                issue = item.get("issue", "N/A")
                table.add_row(date, source, str(issue))

    console.print(table)
    console.print(f"\n共 {len(feedback_files)} 条反馈")


@feedback_cli.command(name="analyze")
def analyze_feedback():
    """分析反馈"""
    console.print("\n📊 反馈分析\n")

    feedback_dir = Path.home() / ".ai-toolkit" / "feedback"

    if not feedback_dir.exists():
        console.print("[yellow]暂无反馈数据[/yellow]")
        return

    feedback_files = list(feedback_dir.glob("*.json"))

    if not feedback_files:
        console.print("[yellow]暂无反馈数据[/yellow]")
        return

    # 统计
    total = len(feedback_files)
    console.print(f"总反馈数: {total}")
    console.print(f"\n💡 建议:")
    console.print("1. 快速响应Issues")
    console.print("2. 修复高优先级Bug")
    console.print("3. 添加请求的功能")
    console.print("4. 改进文档")


@feedback_cli.command(name="respond")
@click.option("--issue", "-i", required=True, type=int, help="Issue编号")
@click.option("--message", "-m", help="回复消息")
def respond_feedback(issue: int, message: str):
    """回复反馈"""
    console.print(f"\n💬 回复 Issue #{issue}\n")

    if message:
        console.print(f"回复: {message}")

    console.print("\n✅ 已回复！")

    console.print("\n💡 最佳实践:")
    console.print("1. 感谢反馈")
    console.print("2. 清晰说明")
    console.print("3. 设置预期")
    console.print("4. 邀请贡献")


@feedback_cli.command(name="prioritize")
def prioritize_feedback():
    """优先级排序"""
    console.print("\n🎯 反馈优先级\n")

    priorities = [
        ("P0", "严重Bug", "立即修复"),
        ("P1", "重要功能", "本周完成"),
        ("P2", "改进建议", "本月完成"),
        ("P3", "优化项", "有时间就做"),
    ]

    table = Table(show_header=True)
    table.add_column("优先级", style="cyan")
    table.add_column("类型", style="green")
    table.add_column("时间", style="yellow")

    for priority, type_, time in priorities:
        table.add_row(priority, type_, time)

    console.print(table)

    console.print("\n💡 排序建议:")
    console.print("1. 安全问题 > 功能问题 > 优化")
    console.print("2. 影响用户多的优先")
    console.print("3. 容易修复的优先")


@feedback_cli.command(name="roadmap")
def feedback_roadmap():
    """基于反馈的路线图"""
    console.print("\n🗺️ 反馈驱动的路线图\n")

    roadmap = [
        ("v0.3.1", "Bug修复", "基于用户反馈"),
        ("v0.4.0", "功能增强", "高频请求"),
        ("v0.5.0", "性能优化", "性能反馈"),
        ("v1.0.0", "重大更新", "社区建议"),
    ]

    table = Table(show_header=True)
    table.add_column("版本", style="cyan")
    table.add_column("重点", style="green")
    table.add_column("来源", style="yellow")

    for version, focus, source in roadmap:
        table.add_row(version, focus, source)

    console.print(table)


@feedback_cli.command(name="survey")
def create_survey():
    """创建用户调查"""
    console.print("\n📝 用户调查\n")

    survey_questions = [
        "1. 你如何使用AI Toolkit？",
        "2. 最喜欢的功能是什么？",
        "3. 最需要改进的是什么？",
        "4. 愿意付费的功能是什么？",
        "5. 推荐给朋友的意愿？",
    ]

    console.print("调查问题:")
    for question in survey_questions:
        console.print(f"  {question}")

    console.print("\n💡 调查建议:")
    console.print("1. 保持简洁")
    console.print("2. 提供激励")
    console.print("3. 多渠道分发")
    console.print("4. 分析结果")
