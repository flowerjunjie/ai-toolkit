"""
插件管理命令
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from ai_toolkit.core.plugin import get_plugin_manager, Plugin

console = Console()


@click.group(name="plugin")
def plugin_cli():
    """管理插件"""
    pass


@plugin_cli.command(name="list")
def list_plugins():
    """列出所有插件"""
    manager = get_plugin_manager()

    plugins = manager.list_plugins()

    if not plugins:
        console.print("[yellow]暂无插件[/yellow]")
        console.print("提示: 将插件放到 ~/.ai-toolkit/plugins/ 目录")
        return

    table = Table(title="🔌 插件列表", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("版本", style="green")
    table.add_column("描述", style="yellow")
    table.add_column("作者", style="blue")
    table.add_column("状态", style="magenta")

    for plugin in plugins:
        status = "✅ 启用" if plugin["enabled"] else "❌ 禁用"
        table.add_row(
            plugin["name"],
            plugin["version"],
            plugin["description"][:30],
            plugin["author"] or "Unknown",
            status,
        )

    console.print(table)
    console.print(f"\n共 {len(plugins)} 个插件")


@plugin_cli.command(name="load")
@click.argument("plugin_path", type=click.Path(exists=True))
def load_plugin(plugin_path: str):
    """加载插件"""
    manager = get_plugin_manager()

    plugin_file = Path(plugin_path)
    manager.load_plugin(plugin_file)

    console.print(f"✅ 插件已加载: {plugin_file.name}")


@plugin_cli.command(name="unload")
@click.argument("name")
def unload_plugin(name: str):
    """卸载插件"""
    manager = get_plugin_manager()

    manager.unload_plugin(name)

    console.print(f"✅ 插件已卸载: {name}")


@plugin_cli.command(name="reload")
def reload_plugins():
    """重新加载所有插件"""
    manager = get_plugin_manager()

    # 清空现有插件
    manager.plugins.clear()

    # 重新加载
    manager.load_plugins()

    console.print(f"✅ 已重新加载 {len(manager.plugins)} 个插件")


@plugin_cli.command(name="create")
@click.argument("name")
@click.option("--description", "-d", default="", help="插件描述")
@click.option("--author", "-a", default="", help="作者")
def create_plugin(name: str, description: str, author: str):
    """创建插件模板"""
    plugins_dir = Path.home() / ".ai-toolkit" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    plugin_file = plugins_dir / f"{name}.py"

    template = f'''"""
{name} 插件
"""

from ai_toolkit.core.plugin import Plugin


class {name.capitalize()}Plugin(Plugin):
    """{name} 插件"""

    name = "{name}"
    version = "1.0.0"
    description = "{description}"
    author = "{author}"

    def on_load(self):
        """插件加载时调用"""
        print(f"[{{self.name}}] 插件已加载")

    def on_unload(self):
        """插件卸载时调用"""
        print(f"[{{self.name}}] 插件已卸载")

    def on_command(self, command, *args, **kwargs):
        """
        命令处理

        Args:
            command: 命令名称
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            命令执行结果
        """
        if command == "hello":
            return f"Hello from {{self.name}}!"

        return None
'''

    with open(plugin_file, "w", encoding="utf-8") as f:
        f.write(template)

    console.print(f"✅ 插件模板已创建: {plugin_file}")
    console.print(f"   插件名称: {name}")
    console.print(f"\n使用方法:")
    console.print(f"   1. 编辑插件文件: {plugin_file}")
    console.print(f"   2. 加载插件: ai-toolkit plugin load {plugin_file}")
    console.print(f"   3. 使用插件: ai-toolkit plugin run {name} hello")
'''

    with open(plugin_file, "w", encoding="utf-8") as f:
        f.write(template)

    console.print(f"✅ 插件模板已创建: {plugin_file}")
    console.print(f"\n编辑插件文件，然后运行: ai-toolkit plugin reload")


@plugin_cli.command(name="run")
@click.argument("plugin_name")
@click.argument("command")
@click.argument("args", nargs=-1)
def run_plugin(plugin_name: str, command: str, args: tuple):
    """运行插件命令"""
    manager = get_plugin_manager()

    results = manager.execute_command(command, *args)

    if not results:
        console.print(f"[yellow]插件 '{plugin_name}' 没有响应命令: {command}[/yellow]")
        return

    for result in results:
        if "error" in result:
            console.print(f"[red][{result['plugin']}] 错误: {result['error']}[/red]")
        else:
            console.print(f"[cyan][{result['plugin']}][/cyan] {result['result']}")
