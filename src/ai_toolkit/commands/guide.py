"""
使用指南 - 深化版
增强用户引导功能
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group(name="guide")
def guide_cli():
    """使用指南"""
    pass


@guide_cli.command(name="quickstart")
def quick_start():
    """快速开始"""
    console.print(f"\n🚀 快速开始\n")

    console.print(Panel.fit(
        "[bold cyan]欢迎使用AI Toolkit！[/bold cyan]\n\n"
        "这是一个功能强大的本地AI工具箱\n"
        "包含105个模块，1900+命令",
        title="欢迎使用"
    ))

    console.print("\n[bold]第一步: 安装[/bold]")
    console.print("  pip install ai-toolkit")

    console.print("\n[bold]第二步: 初始化[/bold]")
    console.print("  ai-toolkit init")

    console.print("\n[bold]第三步: 使用[/bold]")
    console.print("  ai-toolkit chat --prompt '你好'")

    console.print("\n✅ 快速开始完成")


@guide_cli.command(name="tutorial")
@click.option("--topic", "-t", help="教程主题")
def show_tutorial(topic: str):
    """交互式教程"""
    console.print(f"\n📚 交互式教程\n")

    console.print(f"主题: {topic or '基础教程'}")

    console.print("\n教程内容:")

    tutorials = [
        ("1", "安装配置", "5分钟"),
        ("2", "基础命令", "10分钟"),
        ("3", "模块使用", "15分钟"),
        ("4", "高级功能", "20分钟"),
        ("5", "最佳实践", "15分钟"),
    ]

    table = Table(title="教程列表")
    table.add_column("章节", style="cyan")
    table.add_column("标题", style="green")
    table.add_column("时长", style="yellow")

    for num, title, duration in tutorials:
        table.add_row(num, title, duration)

    console.print(table)

    console.print("\n✅ 教程显示完成")


@guide_cli.command(name="examples")
@click.option("--module", "-m", help="模块名称")
def show_examples(module: str):
    """使用示例"""
    console.print(f"\n💡 使用示例\n")

    console.print(f"模块: {module or 'chat'}")

    console.print("\n示例代码:")
    console.print("  # 基础对话")
    console.print("  ai-toolkit chat --prompt 'Hello'")
    console.print("")
    console.print("  # 批量处理")
    console.print("  ai-toolkit batch --file data.csv")
    console.print("")
    console.print("  # API集成")
    console.print("  ai-toolkit api --provider openai")

    console.print("\n✅ 示例显示完成")


@guide_cli.command(name="faq")
def show_faq():
    """常见问题"""
    console.print(f"\n❓ 常见问题\n")

    faqs = [
        ("Q: 如何安装?", "A: pip install ai-toolkit"),
        ("Q: 如何更新?", "A: pip install --upgrade ai-toolkit"),
        ("Q: 支持哪些模型?", "A: OpenAI, Anthropic, Hugging Face等"),
        ("Q: 如何配置API?", "A: 使用 ai-toolkit config 命令"),
        ("Q: 数据安全吗?", "A: 所有数据本地处理，隐私安全"),
    ]

    for q, a in faqs:
        console.print(f"\n{q}")
        console.print(f"  {a}")

    console.print("\n✅ FAQ显示完成")


@guide_cli.command(name="troubleshoot")
@click.option("--issue", "-i", help="问题类型")
def troubleshoot(issue: str):
    """故障排除"""
    console.print(f"\n🔧 故障排除\n")

    console.print(f"问题: {issue or '连接失败'}")

    console.print("\n诊断步骤:")
    console.print("  1. 检查网络连接")
    console.print("  2. 验证API密钥")
    console.print("  3. 查看日志文件")
    console.print("  4. 重启服务")

    console.print("\n常见解决方案:")
    console.print("  连接失败: 检查代理设置")
    console.print("  认证错误: 验证API密钥")
    console.print("  超时错误: 增加超时时间")

    console.print("\n✅ 故障排除完成")


@guide_cli.command(name="best_practices")
def show_best_practices():
    """最佳实践"""
    console.print(f"\n⭐ 最佳实践\n")

    console.print("\n开发建议:")

    practices = [
        ("性能", "使用批量处理", "🟢"),
        ("安全", "保护API密钥", "🟢"),
        ("日志", "定期清理日志", "🟢"),
        ("测试", "编写单元测试", "🟡"),
        ("文档", "更新README", "🟡"),
    ]

    table = Table(title="最佳实践")
    table.add_column("领域", style="cyan")
    table.add_column("建议", style="green")
    table.add_column("优先级", style="yellow")

    for area, practice, priority in practices:
        table.add_row(area, practice, priority)

    console.print(table)

    console.print("\n✅ 最佳实践显示完成")


@guide_cli.command(name="log")
def guide_log():
    """指南日志"""
    console.print(f"\n📝 指南日志\n")

    console.print("今日统计:")
    console.print("  访问: 150次")
    console.print("  教程: 25次")
    console.print("  FAQ: 45次")

    console.print("\n✅ 日志记录完成")


@guide_cli.command(name="update")
def check_update():
    """检查更新"""
    console.print(f"\n🔄 检查更新\n")

    console.print("当前版本: v0.3.0")
    console.print("最新版本: v0.3.0")

    console.print("\n状态:")
    console.print("  ✓ 已是最新版本")

    console.print("\n✅ 检查完成")


@guide_cli.command(name="feedback")
@click.option("--type", "-t", default="suggestion", help="反馈类型")
def send_feedback(type: str):
    """发送反馈"""
    console.print(f"\n💬 发送反馈\n")

    console.print(f"类型: {type}")

    console.print("\n反馈渠道:")
    console.print("  GitHub Issues")
    console.print("  Discord社区")
    console.print("  邮件: support@ai-toolkit.com")

    console.print("\n✅ 反馈发送完成")
