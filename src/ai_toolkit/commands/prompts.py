"""
Prompt模板管理命令
"""

import json
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="prompts")
def prompts_cli():
    """管理Prompt模板"""
    pass


@prompts_cli.command(name="list")
def list_prompts():
    """列出所有Prompt模板"""
    config = get_config()

    prompts_dir = config.prompts_dir
    if not prompts_dir.exists():
        console.print("[yellow]未找到Prompt模板目录[/yellow]")
        return

    prompt_files = list(prompts_dir.glob("*.json"))

    if not prompt_files:
        console.print("[yellow]暂无Prompt模板[/yellow]")
        console.print("提示: 使用 [cyan]ai-toolkit prompts add <name>[/cyan] 创建模板")
        return

    table = Table(title="📝 Prompt模板", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("描述", style="green")
    table.add_column("创建时间", style="yellow")
    table.add_column("变量", style="blue")

    for prompt_file in sorted(prompt_files):
        with open(prompt_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        name = data.get("name", prompt_file.stem)
        description = data.get("description", "")[:30]
        created = data.get("created_at", "")[:10]
        variables = ", ".join(data.get("variables", []))

        table.add_row(name, description, created, variables)

    console.print(table)
    console.print(f"\n共 {len(prompt_files)} 个模板")


@prompts_cli.command(name="add")
@click.argument("name")
@click.argument("content")
@click.option("--description", "-d", default="", help="模板描述")
def add_prompt(name: str, content: str, description: str):
    """添加一个Prompt模板"""
    config = get_config()
    config.prompts_dir.mkdir(parents=True, exist_ok=True)

    # 解析变量（使用 {variable} 格式）
    import re

    variables = re.findall(r"\{(\w+)\}", content)

    prompt_data = {
        "name": name,
        "description": description,
        "content": content,
        "variables": list(set(variables)),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    prompt_file = config.prompts_dir / f"{name}.json"
    with open(prompt_file, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=2, ensure_ascii=False)

    console.print(f"✅ Prompt模板 [cyan]{name}[/cyan] 已创建")

    if variables:
        console.print(f"   检测到变量: [yellow]{', '.join(variables)}[/yellow]")


@prompts_cli.command(name="run")
@click.argument("name")
@click.option("--vars", "-v", multiple=True, help="变量值，格式: key=value")
def run_prompt(name: str, vars: tuple):
    """运行一个Prompt模板"""
    config = get_config()

    prompt_file = config.prompts_dir / f"{name}.json"
    if not prompt_file.exists():
        console.print(f"[red]未找到模板: {name}[/red]")
        return

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

    content = prompt_data["content"]
    variables = prompt_data.get("variables", [])

    # 解析变量值
    var_dict = {}
    for var in vars:
        if "=" in var:
            key, value = var.split("=", 1)
            var_dict[key] = value

    # 检查必需变量
    missing_vars = [v for v in variables if v not in var_dict]
    if missing_vars:
        console.print(f"[yellow]缺少必需变量: {', '.join(missing_vars)}[/yellow]")
        console.print("使用 --vars key=value 格式提供变量")
        return

    # 渲染模板
    try:
        rendered = content.format(**var_dict)
    except KeyError as e:
        console.print(f"[red]变量错误: {e}[/red]")
        return

    console.print(Panel(rendered, title=f"📝 {name}", border_style="cyan"))

    # 如果需要，可以继续发送到模型
    # TODO: 添加 --run-with-model 选项


@prompts_cli.command(name="show")
@click.argument("name")
def show_prompt(name: str):
    """显示Prompt模板详情"""
    config = get_config()

    prompt_file = config.prompts_dir / f"{name}.json"
    if not prompt_file.exists():
        console.print(f"[red]未找到模板: {name}[/red]")
        return

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

    console.print(
        Panel(
            f"""[cyan]名称:[/cyan] {prompt_data['name']}
[cyan]描述:[/cyan] {prompt_data.get('description', 'N/A')}
[cyan]变量:[/cyan] {', '.join(prompt_data.get('variables', []))}
[cyan]创建时间:[/cyan] {prompt_data.get('created_at', 'N/A')}
[cyan]更新时间:[/cyan] {prompt_data.get('updated_at', 'N/A')}""",
            title=f"📝 {name}",
            border_style="cyan",
        )
    )

    console.print("\n[bold]内容:[/bold]")
    syntax = Syntax(prompt_data["content"], "text", theme="monokai", line_numbers=True)
    console.print(syntax)


@prompts_cli.command(name="edit")
@click.argument("name")
@click.argument("content")
@click.option("--description", "-d", help="更新描述")
def edit_prompt(name: str, content: str, description: str = None):
    """编辑Prompt模板"""
    config = get_config()

    prompt_file = config.prompts_dir / f"{name}.json"
    if not prompt_file.exists():
        console.print(f"[red]未找到模板: {name}[/red]")
        return

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

    # 更新内容
    prompt_data["content"] = content
    prompt_data["updated_at"] = datetime.now().isoformat()

    if description:
        prompt_data["description"] = description

    # 重新解析变量
    import re

    variables = re.findall(r"\{(\w+)\}", content)
    prompt_data["variables"] = list(set(variables))

    with open(prompt_file, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=2, ensure_ascii=False)

    console.print(f"✅ Prompt模板 [cyan]{name}[/cyan] 已更新")


@prompts_cli.command(name="delete")
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="强制删除")
def delete_prompt(name: str, force: bool):
    """删除Prompt模板"""
    if not force:
        if not click.confirm(f"确定要删除模板 '{name}' 吗？"):
            console.print("已取消")
            return

    config = get_config()
    prompt_file = config.prompts_dir / f"{name}.json"

    if not prompt_file.exists():
        console.print(f"[red]未找到模板: {name}[/red]")
        return

    prompt_file.unlink()
    console.print(f"✅ Prompt模板 [cyan]{name}[/cyan] 已删除")
