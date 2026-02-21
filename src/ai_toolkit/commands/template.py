"""
模板命令 - 预设模板库
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group(name="template")
def template_cli():
    """预设模板库"""
    pass


# 预设模板
PRESET_TEMPLATES = {
    "python-dev": {
        "name": "Python开发专家",
        "description": "专业的Python开发者，帮助编写、优化、调试代码",
        "content": """你是一个专业的Python开发者助手。

你的职责：
1. 编写符合PEP 8规范的代码
2. 代码要有清晰的注释和文档字符串
3. 考虑性能和最佳实践
4. 处理边界情况和错误
5. 提供优化建议

请用中文回答，代码使用markdown格式。

任务: {task}
""",
    },
    "code-review": {
        "name": "代码审查员",
        "description": "专业的代码审查员，发现潜在问题",
        "content": """你是一个专业的代码审查员。

请审查以下代码，重点关注：
1. **潜在Bug**
2. **性能问题**
3. **安全问题**
4. **代码风格**
5. **改进建议**

请用中文回答，给出具体建议。

代码:
```python
{code}
```
""",
    },
    "writer": {
        "name": "技术写作助手",
        "description": "技术文档和教程写作",
        "content": """你是一个专业的技术写作助手。

请根据以下要求创建内容：
- 结构清晰
- 技术准确
- 易于理解
- 适当使用示例

主题: {topic}
篇幅: {length}
""",
    },
    "explainer": {
        "name": "代码解释器",
        "description": "用通俗易懂的语言解释代码",
        "content": """请用通俗易懂的语言解释以下代码。

重点说明：
- 代码的功能
- 工作原理
- 关键技术点
- 实际应用场景

代码:
```python
{code}
```
""",
    },
    "debugger": {
        "name": "调试专家",
        "description": "帮助诊断和修复代码问题",
        "content": """你是一个调试专家。

请帮助诊断以下问题：

错误信息:
```
{error}
```

代码:
```python
{code}
```

请分析可能的原因和解决方案。
""",
    },
}


@template_cli.command(name="list")
def list_templates():
    """列出所有预设模板"""
    table = Table(title="📚 预设模板库", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("描述", style="green")
    table.add_column("变量", style="yellow")

    for key, template in PRESET_TEMPLATES.items():
        import re

        variables = re.findall(r"\{(\w+)\}", template["content"])
        table.add_row(
            key,
            template["description"][:30],
            ", ".join(variables) if variables else "无",
        )

    console.print(table)
    console.print(f"\n共 {len(PRESET_TEMPLATES)} 个模板")
    console.print("\n使用: ai-toolkit template use <模板名>")
    console.print("查看: ai-toolkit template show <模板名>")


@template_cli.command(name="use")
@click.argument("template_name")
@click.argument("args", nargs=-1)
def use_template(template_name: str, args: tuple):
    """使用预设模板"""
    if template_name not in PRESET_TEMPLATES:
        console.print(f"[red]模板不存在: {template_name}[/red]")
        console.print(f"\n可用模板:")
        for key in PRESET_TEMPLATES.keys():
            console.print(f"  - {key}")
        return

    template = PRESET_TEMPLATES[template_name]

    # 获取用户输入
    console.print(f"\n📋 模板: {template['name']}")
    console.print(f"📝 描述: {template['description']}\n")
    console.print("提示: 直接输入你的问题/代码/任务，按 Ctrl+D 结束\n")

    import sys

    user_input = []
    console.print("👤 输入:\n")

    try:
        for line in sys.stdin:
            user_input.append(line)
    except KeyboardInterrupt:
        pass

    if not user_input:
        console.print("\n[yellow]已取消[/yellow]")
        return

    content = "\n".join(user_input).strip()

    # 使用模板
    from ai_toolkit.core.llm_client import LLMClient

    client = LLMClient()

    formatted = template["content"].replace("{content}", content)

    console.print("\n🤖 正在生成...\n")

    try:
        result = client.generate(formatted, max_tokens=2000)
        console.print(result)
        console.print("\n✅ 生成完成！")
    except Exception as e:
        console.print(f"\n[red]生成失败: {e}[/red]")


@template_cli.command(name="show")
@click.argument("template_name")
def show_template(template_name: str):
    """显示模板详情"""
    if template_name not in PRESET_TEMPLATES:
        console.print(f"[red]模板不存在: {template_name}[/red]")
        return

    template = PRESET_TEMPLATES[template_name]

    console.print(Panel(
        f"""[cyan]名称:[/cyan] {template['name']}
[cyan]描述:[/cyan] {template['description']}

[cyan]变量:[/cyan]
{template.get('variables', '无')}

[cyan]内容:[/cyan]
{template['content']}""",
        title=f"📋 {template_name}",
        border_style="cyan",
    ))
