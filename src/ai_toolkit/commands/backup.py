"""
备份恢复命令
"""

import click
import shutil
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()


@click.group(name="backup")
def backup_cli():
    """备份和恢复"""
    pass


@backup_cli.command(name="create")
@click.option("--target", "-t", type=click.Path(), help="备份目标目录")
@click.option("--name", "-n", help="备份名称")
def create_backup(target: str, name: str):
    """创建备份"""
    from ai_toolkit.core.config import get_config

    config = get_config()

    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")

    if target:
        backup_dir = Path(target)
    else:
        backup_dir = config.data_dir / "backups" / name

    console.print(f"📦 创建备份: {name}")
    console.print(f"目标: {backup_dir}\n")

    # 要备份的目录
    items_to_backup = [
        (config.prompts_dir, "prompts"),
        (config.rag_dir, "rag"),
        (config.models_dir, "models"),
    ]

    for source_dir, item_name in items_to_backup:
        if source_dir.exists():
            dest_dir = backup_dir / item_name
            console.print(f"备份 {item_name}...")

            if dest_dir.exists():
                shutil.rmtree(dest_dir)

            shutil.copytree(source_dir, dest_dir)
            console.print(f"  ✅ {item_name} -> {dest_dir}")
        else:
            console.print(f"  ⏭️  {item_name} (不存在)")

    # 备份配置文件
    if config.config_path.exists():
        import json

        backup_config = backup_dir / "config.json"
        shutil.copy2(config.config_path, backup_config)
        console.print(f"  ✅ config.json")

    console.print(f"\n✅ 备份完成: {backup_dir}")


@backup_cli.command(name="list")
def list_backups():
    """列出所有备份"""
    from ai_toolkit.core.config import get_config

    config = get_config()
    backup_dir = config.data_dir / "backups"

    if not backup_dir.exists():
        console.print("[yellow]暂无备份[/yellow]")
        return

    backups = [d for d in backup_dir.iterdir() if d.is_dir()]

    if not backups:
        console.print("[yellow]暂无备份[/yellow]")
        return

    from rich.table import Table

    table = Table(title="📦 备份列表", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("时间", style="green")
    table.add_column("大小", style="yellow")

    for bk in sorted(backups, reverse=True):
        # 计算大小
        size = sum(f.stat().st_size for f in bk.rglob("*") if f.is_file())
        size_mb = size / (1024 * 1024)

        table.add_row(
            bk.name,
            bk.stat().st_mtime,
            f"{size_mb:.2f} MB",
        )

    console.print(table)
    console.print(f"\n共 {len(backups)} 个备份")


@backup_cli.command(name="restore")
@click.argument("name")
@click.option("--target", "-t", type=click.Path(), help="恢复目标目录")
def restore_backup(name: str, target: str):
    """恢复备份"""
    from ai_toolkit.core.config import get_config

    config = get_config()
    backup_dir = config.data_dir / "backups" / name

    if not backup_dir.exists():
        console.print(f"[red]备份不存在: {name}[/red]")
        return

    console.print(f"🔄 恢复备份: {name}")
    console.print(f"来源: {backup_dir}\n")

    if target:
        restore_target = Path(target)
    else:
        restore_target = config.data_dir / "restored" / name

    # 确认
    if not click.confirm(f"这将覆盖 {restore_target}，确定吗？"):
        console.print("已取消")
        return

    # 恢复文件
    for item in backup_dir.iterdir():
        if item.is_dir():
            target_item = restore_target / item.name
            console.print(f"恢复 {item.name}...")

            if target_item.exists():
                shutil.rmtree(target_item)

            shutil.copytree(item, target_item)
            console.print(f"  ✅ {item.name} -> {target_item}")

    console.print(f"\n✅ 恢复完成: {restore_target}")
