"""
命令别名管理
"""

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="alias")
def alias_cli():
    """管理命令别名"""
    pass


@alias_cli.command(name="list")
def list_aliases():
    """列出所有别名"""
    config = get_config()
    alias_file = config.data_dir / "aliases.json"

    if not alias_file.exists():
        console.print("[yellow]暂无别名[/yellow]")
        console.print("提示: 使用 [cyan]ai-toolkit alias add <name> <command>[/cyan] 创建别名")
        return

    with open(alias_file, "r", encoding="utf-8") as f:
        aliases = json.load(f)

    if not aliases:
        console.print("[yellow]暂无别名[/yellow]")
        return

    table = Table(title="📝 命令别名", show_header=True)
    table.add_column("别名", style="cyan")
    table.add_column("原始命令", style="green")
    table.add_column("描述", style="yellow")

    for name, cmd in aliases.items():
        command = cmd.get("command", "")
        description = cmd.get("description", "")
        table.add_row(name, command, description)

    console.print(table)
    console.print(f"\n共 {len(aliases)} 个别名")


@alias_cli.command(name="add")
@click.argument("name")
@click.argument("command")
@click.option("--description", "-d", default="", help="别名描述")
def add_alias(name: str, command: str, description: str):
    """添加别名"""
    config = get_config()
    alias_file = config.data_dir / "aliases.json"

    # 加载现有别名
    if alias_file.exists():
        with open(alias_file, "r", encoding="utf-8") as f:
            aliases = json.load(f)
    else:
        aliases = {}

    # 添加别名
    aliases[name] = {
        "command": command,
        "description": description,
    }

    # 保存
    alias_file.parent.mkdir(parents=True, exist_ok=True)
    with open(alias_file, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2, ensure_ascii=False)

    console.print(f"✅ 别名 [cyan]{name}[/cyan] 已添加")
    console.print(f"   原始命令: {command}")


@alias_cli.command(name="remove")
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="强制删除")
def remove_alias(name: str, force: bool):
    """删除别名"""
    if not force:
        if not click.confirm(f"确定要删除别名 '{name}' 吗？"):
            console.print("已取消")
            return

    config = get_config()
    alias_file = config.data_dir / "aliases.json"

    if not alias_file.exists():
        console.print(f"[red]别名文件不存在[/red]")
        return

    with open(alias_file, "r", encoding="utf-8") as f:
        aliases = json.load(f)

    if name not in aliases:
        console.print(f"[red]别名不存在: {name}[/red]")
        return

    del aliases[name]

    with open(alias_file, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2, ensure_ascii=False)

    console.print(f"✅ 别名 [cyan]{name}[/cyan] 已删除")


@alias_cli.command(name="run")
@click.argument("name")
@click.argument("args", nargs=-1)
def run_alias(name: str, args: tuple):
    """运行别名"""
    config = get_config()
    alias_file = config.data_dir / "aliases.json"

    if not alias_file.exists():
        console.print(f"[red]别名文件不存在[/red]")
        return

    with open(alias_file, "r", encoding="utf-8") as f:
        aliases = json.load(f)

    if name not in aliases:
        console.print(f"[red]别名不存在: {name}[/red]")
        console.print(f"使用 [cyan]ai-toolkit alias list[/cyan] 查看所有别名")
        return

    command = aliases[name]["command"]

    # 替换参数
    if args:
        command = command.replace("$*", " ".join(args))
        for i, arg in enumerate(args, 1):
            command = command.replace(f"${i}", arg)

    # 执行命令
    import subprocess

    console.print(f"执行: [dim]{command}[/dim]\n")
    result = subprocess.run(command, shell=True)
    return result.returncode


# 默认别名
DEFAULT_ALIASES = {
    "mls": {"command": "ai-toolkit models list", "description": "列出模型"},
    "mpull": {"command": "ai-toolkit models pull $*", "description": "下载模型"},
    "mrun": {"command": "ai-toolkit models run $*", "description": "运行模型"},
    "pls": {"command": "ai-toolkit prompts list", "description": "列出Prompt模板"},
    "padd": {"command": "ai-toolkit prompts add $*", "description": "添加Prompt模板"},
    "prun": {"command": "ai-toolkit prompts run $*", "description": "运行Prompt模板"},
    "rls": {"command": "ai-toolkit rag2 list", "description": "列出RAG知识库"},
    "rquery": {"command": "ai-toolkit rag2 query $*", "description": "查询RAG"},
    "gen": {"command": "ai-toolkit coding generate $*", "description": "生成代码"},
    "review": {"command": "ai-toolkit coding review $*", "description": "代码审查"},
}


def init_default_aliases():
    """初始化默认别名"""
    config = get_config()
    alias_file = config.data_dir / "aliases.json"

    if alias_file.exists():
        return

    alias_file.parent.mkdir(parents=True, exist_ok=True)

    with open(alias_file, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_ALIASES, f, indent=2, ensure_ascii=False)
