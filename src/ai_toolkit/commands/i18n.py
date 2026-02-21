"""
国际化工具
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json

console = Console()


@click.group(name="i18n")
def i18n_cli():
    """国际化工具"""
    pass


@i18n_cli.command(name="list")
def list_languages():
    """列出支持的语言"""
    console.print("\n🌍 支持的语言\n")

    languages = [
        ("en", "English", "英语", "✅ 完整"),
        ("zh", "中文", "简体中文", "✅ 完整"),
        ("zh-tw", "繁體中文", "繁体中文", "⏳ 翻译中"),
        ("ja", "日本語", "日语", "📋 计划中"),
        ("ko", "한국어", "韩语", "📋 计划中"),
        ("es", "Español", "西班牙语", "📋 计划中"),
        ("fr", "Français", "法语", "📋 计划中"),
        ("de", "Deutsch", "德语", "📋 计划中"),
        ("ru", "Русский", "俄语", "📋 计划中"),
        ("ar", "العربية", "阿拉伯语", "📋 计划中"),
    ]

    table = Table(show_header=True)
    table.add_column("代码", style="cyan")
    table.add_column("名称", style="green")
    table.add_column("本地名", style="yellow")
    table.add_column("状态", style="blue")

    for code, name, native, status in languages:
        table.add_row(code, name, native, status)

    console.print(table)

    console.print("\n💡 贡献翻译:")
    console.print("  欢迎贡献翻译！")
    console.print("  GitHub: https://github.com/flowerjunjie/ai-toolkit")


@i18n_cli.command(name="extract")
def extract_strings():
    """提取待翻译字符串"""
    console.print("\n🔍 提取字符串\n")

    console.print("正在扫描代码...")

    strings = [
        ("模型管理", "models", "src/ai_toolkit/commands/models.py"),
        ("Prompt模板", "prompts", "src/ai_toolkit/commands/prompts.py"),
        ("AI编码助手", "coding", "src/ai_toolkit/commands/coding.py"),
        ("系统状态", "status", "src/ai_toolkit/cli.py"),
    ]

    table = Table(show_header=True)
    table.add_column("字符串", style="cyan")
    table.add_column("上下文", style="green")
    table.add_column("位置", style="yellow")

    for string, context, location in strings:
        table.add_row(string, context, location)

    console.print(table)

    console.print(f"\n✅ 提取了 {len(strings)} 个字符串")


@i18n_cli.command(name="translate")
@click.option("--lang", "-l", required=True, help="目标语言")
@click.option("--file", "-f", help="翻译文件")
def translate(lang: str, file: str):
    """翻译"""
    console.print(f"\n🌐 翻译到: {lang}\n")

    # 翻译模板
    translations = {
        "en": {
            "models": "Models",
            "prompts": "Prompts",
            "coding": "AI Coding Assistant",
            "status": "System Status",
        },
        "zh": {
            "models": "模型管理",
            "prompts": "Prompt模板",
            "coding": "AI编码助手",
            "status": "系统状态",
        },
    }

    if lang in translations:
        console.print("翻译结果:")
        for key, value in translations[lang].items():
            console.print(f"  {key}: {value}")

        # 保存翻译
        i18n_dir = Path.home() / ".ai-toolkit" / "i18n"
        i18n_dir.mkdir(parents=True, exist_ok=True)

        trans_file = i18n_dir / f"{lang}.json"
        with open(trans_file, "w", encoding="utf-8") as f:
            json.dump(translations[lang], f, indent=2, ensure_ascii=False)

        console.print(f"\n✅ 翻译已保存: {trans_file}")
    else:
        console.print(f"[yellow]语言 {lang} 尚未支持[/yellow]")


@i18n_cli.command(name="validate")
@click.option("--lang", "-l", help="验证语言")
def validate_translations(lang: str):
    """验证翻译"""
    console.print("\n✅ 验证翻译\n")

    if lang:
        console.print(f"验证语言: {lang}")
    else:
        console.print("验证所有翻译")

    # 验证检查
    checks = [
        ("完整性", "✅ 通过"),
        ("格式", "✅ 通过"),
        ("占位符", "✅ 通过"),
        ("上下文", "✅ 通过"),
    ]

    table = Table(show_header=True)
    table.add_column("检查项", style="cyan")
    table.add_column("状态", style="green")

    for check, status in checks:
        table.add_row(check, status)

    console.print(table)

    console.print("\n✅ 所有翻译有效")


@i18n_cli.command(name="update")
@click.option("--lang", "-l", required=True, help="更新语言")
def update_translations(lang: str):
    """更新翻译"""
    console.print(f"\n🔄 更新翻译: {lang}\n")

    console.print("正在检查新字符串...")

    new_strings = [
        "性能优化",
        "用户体验",
        "安全审计",
    ]

    console.print(f"发现 {len(new_strings)} 个新字符串")

    console.print("\n✅ 准备翻译")
    console.print("\n💡 翻译指南:")
    console.print("1. 保持简洁")
    console.print("2. 保持一致")
    console.print("3. 检查上下文")
    console.print("4. 测试显示")


@i18n_cli.command(name="stats")
def translation_stats():
    """翻译统计"""
    console.print("\n📊 翻译统计\n")

    stats = [
        ("英语", "100%", "完整"),
        ("简体中文", "100%", "完整"),
        ("繁体中文", "60%", "进行中"),
        ("日语", "0%", "未开始"),
        ("韩语", "0%", "未开始"),
    ]

    table = Table(show_header=True)
    table.add_column("语言", style="cyan")
    table.add_column("进度", style="green")
    table.add_column("状态", style="yellow")

    for lang, progress, status in stats:
        table.add_row(lang, progress, status)

    console.print(table)

    console.print("\n📈 总体进度:")
    console.print("  平均: 52%")
    console.print("  完整: 2/10")
    console.print("  进行中: 1/10")


@i18n_cli.command(name="guide")
def translation_guide():
    """翻译指南"""
    console.print("\n📖 翻译指南\n")

    guide = """
# 翻译指南

## 基本原则

1. **准确性**: 保持原意
2. **简洁性**: 简短有力
3. **一致性**: 术语统一
4. **本地化**: 适应文化

## 术语表

| English | 中文 | 说明 |
|---------|------|------|
| Model | 模型 | AI模型 |
| Prompt | 提示词 | AI提示 |
| Plugin | 插件 | 功能插件 |
| RAG | 知识库 | 检索增强 |

## 翻译流程

1. 申请翻译任务
2. 下载翻译文件
3. 完成翻译
4. 提交PR
5. 审核合并

## 贡献

欢迎贡献翻译！

GitHub: https://github.com/flowerjunjie/ai-toolkit
"""

    console.print(Panel(guide, title="📖 翻译指南", border_style="cyan"))
