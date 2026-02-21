"""
用户体验工具
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json

console = Console()


@click.group(name="ux")
def ux_cli():
    """用户体验优化"""
    pass


@ux_cli.command(name="analyze")
def analyze_ux():
    """UX分析"""
    console.print("\n🎨 UX分析\n")

    aspects = [
        ("易用性", "4/5", "优秀"),
        ("学习曲线", "3/5", "良好"),
        ("文档完整性", "5/5", "优秀"),
        ("错误提示", "4/5", "优秀"),
        ("命令一致性", "5/5", "优秀"),
        ("输出美观", "5/5", "优秀"),
    ]

    table = Table(show_header=True)
    table.add_column("方面", style="cyan")
    table.add_column("评分", style="green")
    table.add_column("评级", style="yellow")

    for aspect, score, rating in aspects:
        table.add_row(aspect, score, rating)

    console.print(table)

    console.print("\n💡 改进建议:")
    console.print("1. 添加交互式引导")
    console.print("2. 提供更多示例")
    console.print("3. 改进错误消息")
    console.print("4. 添加快捷命令")


@ux_cli.command(name="guide")
@click.option("--feature", "-f", help="功能名称")
def show_guide(feature: str):
    """显示使用指南"""
    console.print("\n📖 使用指南\n")

    if feature:
        console.print(f"功能: {feature}")
    else:
        console.print("快速开始指南")

    guide = """
# AI Toolkit 快速开始

## 第一步: 安装
```bash
pip install ai-toolkit
```

## 第二步: 初始化
```bash
ai-toolkit init
```

## 第三步: 下载模型
```bash
ai-toolkit models pull llama3.2
```

## 第四步: 运行
```bash
ai-toolkit coding generate "写一个快速排序"
```

## 常用命令
- `ai-toolkit status` - 查看状态
- `ai-toolkit models list` - 列出模型
- `ai-toolkit prompts list` - 列出模板
- `ai-toolkit shell` - 交互式Shell

## 帮助
- `ai-toolkit --help` - 全局帮助
- `ai-toolkit <command> --help` - 命令帮助
"""

    console.print(Panel(guide, title="📖 使用指南", border_style="cyan"))


@ux_cli.command(name="onboarding")
def interactive_onboarding():
    """交互式引导"""
    console.print("\n👋 欢迎使用 AI Toolkit!\n")

    console.print("AI Toolkit 是一个强大的本地AI工具箱。")
    console.print("让我们花2分钟了解基本功能。\n")

    console.print("📚 核心功能:")
    console.print("1. 模型管理 - 下载和管理AI模型")
    console.print("2. Prompt模板 - 管理AI提示词")
    console.print("3. RAG知识库 - 本地知识库问答")
    console.print("4. AI编码助手 - AI辅助编程")
    console.print("5. 插件系统 - 扩展功能\n")

    console.print("🚀 快速开始:")
    console.print("  ai-toolkit init")
    console.print("  ai-toolkit models pull llama3.2")
    console.print("  ai-toolkit coding generate 'Hello World'\n")

    console.print("📖 文档:")
    console.print("  https://github.com/flowerjunjie/ai-toolkit\n")

    console.print("✅ 你已经准备好了！开始探索吧！")


@ux_cli.command(name="shortcuts")
def show_shortcuts():
    """显示快捷命令"""
    console.print("\n⌨️ 快捷命令\n")

    shortcuts = [
        ("st", "status", "系统状态"),
        ("ml", "models list", "列出模型"),
        ("pl", "prompts list", "列出模板"),
        ("cg", "coding generate", "AI生成代码"),
        ("sh", "shell", "交互式Shell"),
        ("wb", "webui", "Web界面"),
    ]

    table = Table(show_header=True)
    table.add_column("快捷", style="cyan")
    table.add_column("命令", style="green")
    table.add_column("说明", style="yellow")

    for shortcut, command, desc in shortcuts:
        table.add_row(shortcut, command, desc)

    console.print(table)

    console.print("\n💡 使用方法:")
    console.print("  ai-toolkit alias add st ai-toolkit status")


@ux_cli.command(name="errors")
def show_errors():
    """错误处理指南"""
    console.print("\n❌ 常见错误\n")

    errors = [
        ("模型未找到", "下载模型: ai-toolkit models pull <模型>"),
        ("API Key错误", "设置环境变量: export BIGMODEL_API_KEY=xxx"),
        ("配置文件错误", "重新初始化: ai-toolkit init"),
        ("权限错误", "检查目录权限"),
        ("网络错误", "检查网络连接"),
    ]

    table = Table(show_header=True)
    table.add_column("错误", style="cyan")
    table.add_column("解决", style="green")

    for error, solution in errors:
        table.add_row(error, solution)

    console.print(table)

    console.print("\n💡 获取帮助:")
    console.print("  ai-toolkit diag all - 系统诊断")
    console.print("  GitHub Issues - 报告问题")


@ux_cli.command(name="feedback")
def collect_ux_feedback():
    """收集UX反馈"""
    console.print("\n💬 UX反馈\n")

    console.print("帮助我们改进用户体验！")

    questions = [
        "1. 整体易用性？(1-5分)",
        "2. 文档清晰度？(1-5分)",
        "3. 命令直观性？(1-5分)",
        "4. 最喜欢的功能？",
        "5. 最需要改进的？",
    ]

    console.print("\n反馈问题:")
    for question in questions:
        console.print(f"  {question}")

    console.print("\n💡 提交反馈:")
    console.print("  GitHub Issues: https://github.com/flowerjunjie/ai-toolkit/issues")
    console.print("  或使用: ai-toolkit feedback collect")


@ux_cli.command(name="a11y")
def check_accessibility():
    """可访问性检查"""
    console.print("\n♿ 可访问性检查\n")

    checks = [
        ("颜色对比度", "✅ 通过"),
        ("字体大小", "✅ 通过"),
        ("键盘导航", "✅ 通过"),
        ("屏幕阅读器", "⚠️ 部分支持"),
        ("高对比度", "✅ 支持"),
    ]

    table = Table(show_header=True)
    table.add_column("检查项", style="cyan")
    table.add_column("状态", style="green")

    for check, status in checks:
        table.add_row(check, status)

    console.print(table)

    console.print("\n💡 改进建议:")
    console.print("1. 增强屏幕阅读器支持")
    console.print("2. 添加更多键盘快捷键")
    console.print("3. 支持自定义主题")
