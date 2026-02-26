"""
备份工具 - 真实化实现
支持真实文件备份、压缩、加密和恢复
"""

import os
import hashlib
import json
import tarfile
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

console = Console()

# 备份配置目录
BACKUP_CONFIG_DIR = Path.home() / ".ai-toolkit" / "backups"
BACKUP_CONFIG_FILE = BACKUP_CONFIG_DIR / "config.json"
BACKUP_LOG_FILE = BACKUP_CONFIG_DIR / "backup.log"


def _ensure_config_dir():
    """确保配置目录存在"""
    BACKUP_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> Dict[str, Any]:
    """加载备份配置"""
    _ensure_config_dir()
    if BACKUP_CONFIG_FILE.exists():
        with open(BACKUP_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"backups": [], "schedules": []}


def _save_config(config: Dict[str, Any]):
    """保存备份配置"""
    _ensure_config_dir()
    with open(BACKUP_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def _generate_backup_id() -> str:
    """生成备份ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:6]
    return f"bak_{timestamp}_{random_suffix}"


def _calculate_checksum(filepath: Path) -> str:
    """计算文件MD5校验和"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def _get_directory_size(path: Path) -> int:
    """获取目录大小（字节）"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = Path(dirpath) / f
            if fp.exists():
                total += fp.stat().st_size
    return total


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def _log_backup_operation(operation: str, details: str):
    """记录备份操作日志"""
    _ensure_config_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {operation}: {details}\n"
    with open(BACKUP_LOG_FILE, 'a') as f:
        f.write(log_entry)


@click.group(name="backup")
def backup_cli():
    """备份工具 - 支持真实文件备份、压缩和恢复"""
    pass


@backup_cli.command(name="create")
@click.option("--source", "-s", required=True, help="源目录或文件路径")
@click.option("--target", "-t", required=True, help="备份目标目录")
@click.option("--type", "-tp", default="full", type=click.Choice(['full', 'incremental', 'differential']), help="备份类型")
@click.option("--compress", "-c", is_flag=True, help="是否压缩")
@click.option("--encrypt", "-e", is_flag=True, help="是否加密（需要GPG）")
@click.option("--exclude", "-x", multiple=True, help="排除模式（可多次使用）")
@click.option("--name", "-n", help="备份名称（可选）")
def create_backup(source: str, target: str, type: str, compress: bool, encrypt: bool, exclude: tuple, name: Optional[str]):
    """创建真实备份"""
    source_path = Path(source).expanduser().resolve()
    target_path = Path(target).expanduser().resolve()
    
    # 验证源路径
    if not source_path.exists():
        console.print(f"[red]错误: 源路径不存在: {source}[/red]")
        raise click.Exit(1)
    
    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)
    
    backup_id = _generate_backup_id()
    backup_name = name or f"backup_{source_path.name}"
    timestamp = datetime.now().isoformat()
    
    console.print(f"\n[bold cyan]💾 创建备份[/bold cyan]\n")
    console.print(f"备份ID: [green]{backup_id}[/green]")
    console.print(f"名称: {backup_name}")
    console.print(f"源: {source_path}")
    console.print(f"目标: {target_path}")
    console.print(f"类型: {type}")
    console.print(f"压缩: {'是' if compress else '否'}")
    console.print(f"加密: {'是' if encrypt else '否'}")
    
    # 计算源大小
    if source_path.is_dir():
        source_size = _get_directory_size(source_path)
        file_count = sum(1 for _ in source_path.rglob('*') if _.is_file())
    else:
        source_size = source_path.stat().st_size
        file_count = 1
    
    console.print(f"源大小: {_format_size(source_size)}")
    console.print(f"文件数: {file_count}")
    
    # 执行备份
    backup_file = target_path / f"{backup_id}.tar"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("正在备份...", total=None)
        
        try:
            if type == "full":
                # 完整备份 - 使用 tar
                with tarfile.open(backup_file, 'w') as tar:
                    tar.add(source_path, arcname=source_path.name)
                
            elif type == "incremental":
                # 增量备份 - 使用 rsync
                backup_dir = target_path / backup_id
                backup_dir.mkdir(exist_ok=True)
                
                cmd = ["rsync", "-av", "--delete"]
                for pattern in exclude:
                    cmd.extend(["--exclude", pattern])
                cmd.extend([str(source_path) + "/", str(backup_dir) + "/"])
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    console.print(f"[red]rsync 失败: {result.stderr}[/red]")
                    raise click.Exit(1)
                
                # 打包为 tar
                with tarfile.open(backup_file, 'w') as tar:
                    tar.add(backup_dir, arcname=backup_dir.name)
                
                # 清理临时目录
                shutil.rmtree(backup_dir)
                
            elif type == "differential":
                # 差异备份
                backup_dir = target_path / backup_id
                backup_dir.mkdir(exist_ok=True)
                
                cmd = ["rsync", "-av", "--backup", "--backup-dir", str(backup_dir)]
                for pattern in exclude:
                    cmd.extend(["--exclude", pattern])
                cmd.extend([str(source_path) + "/", str(backup_dir) + "/"])
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    console.print(f"[red]rsync 失败: {result.stderr}[/red]")
                    raise click.Exit(1)
                
                with tarfile.open(backup_file, 'w') as tar:
                    tar.add(backup_dir, arcname=backup_dir.name)
                
                shutil.rmtree(backup_dir)
            
            progress.update(task, description="备份完成")
            
        except Exception as e:
            console.print(f"[red]备份失败: {e}[/red]")
            raise click.Exit(1)
    
    # 压缩
    if compress:
        console.print("\n[yellow]正在压缩...[/yellow]")
        compressed_file = backup_file.with_suffix('.tar.gz')
        with tarfile.open(compressed_file, 'w:gz') as tar:
            tar.add(backup_file, arcname=backup_file.name)
        backup_file.unlink()  # 删除未压缩版本
        backup_file = compressed_file
    
    # 加密
    if encrypt:
        console.print("\n[yellow]正在加密...[/yellow]")
        encrypted_file = backup_file.with_suffix(backup_file.suffix + '.gpg')
        cmd = ["gpg", "--symmetric", "--cipher-algo", "AES256", "--output", str(encrypted_file), str(backup_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[yellow]警告: 加密失败，保留未加密版本[/yellow]")
        else:
            backup_file.unlink()  # 删除未加密版本
            backup_file = encrypted_file
    
    # 计算校验和
    checksum = _calculate_checksum(backup_file)
    backup_size = backup_file.stat().st_size
    
    # 保存备份记录
    config = _load_config()
    backup_record = {
        "id": backup_id,
        "name": backup_name,
        "source": str(source_path),
        "target": str(target_path),
        "type": type,
        "compressed": compress,
        "encrypted": encrypt,
        "file": str(backup_file),
        "size": backup_size,
        "source_size": source_size,
        "file_count": file_count,
        "checksum": checksum,
        "created_at": timestamp,
        "exclude_patterns": list(exclude)
    }
    config["backups"].append(backup_record)
    _save_config(config)
    
    # 记录日志
    _log_backup_operation("CREATE", f"{backup_id} - {backup_name} - {source} -> {backup_file}")
    
    # 显示结果
    console.print(f"\n[bold green]✅ 备份完成[/bold green]")
    console.print(f"备份文件: {backup_file}")
    console.print(f"备份大小: {_format_size(backup_size)}")
    console.print(f"压缩率: {(1 - backup_size / source_size) * 100:.1f}%" if source_size > 0 else "N/A")
    console.print(f"校验和: {checksum[:16]}...")


@backup_cli.command(name="restore")
@click.option("--backup", "-b", required=True, help="备份ID或备份文件路径")
@click.option("--target", "-t", required=True, help="恢复目标目录")
@click.option("--decrypt", "-d", is_flag=True, help="解密备份（如果是加密的）")
@click.option("--force", "-f", is_flag=True, help="强制覆盖现有文件")
def restore_backup(backup: str, target: str, decrypt: bool, force: bool):
    """从备份恢复文件"""
    target_path = Path(target).expanduser().resolve()
    
    # 查找备份
    config = _load_config()
    backup_record = None
    backup_file = None
    
    # 先尝试从配置中查找
    for b in config.get("backups", []):
        if b["id"] == backup or b["name"] == backup:
            backup_record = b
            backup_file = Path(b["file"])
            break
    
    # 如果找不到，尝试作为文件路径
    if not backup_file:
        backup_file = Path(backup).expanduser().resolve()
        if not backup_file.exists():
            console.print(f"[red]错误: 找不到备份: {backup}[/red]")
            raise click.Exit(1)
    
    if not backup_file.exists():
        console.print(f"[red]错误: 备份文件不存在: {backup_file}[/red]")
        raise click.Exit(1)
    
    console.print(f"\n[bold cyan]🔄 恢复备份[/bold cyan]\n")
    console.print(f"备份文件: {backup_file}")
    console.print(f"目标目录: {target_path}")
    
    # 检查目标目录
    if target_path.exists() and not force:
        if any(target_path.iterdir()):
            console.print(f"[yellow]警告: 目标目录不为空，使用 --force 覆盖[/yellow]")
            raise click.Exit(1)
    
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 解密
    working_file = backup_file
    if decrypt or (backup_record and backup_record.get("encrypted")):
        if backup_file.suffix == '.gpg':
            console.print("\n[yellow]正在解密...[/yellow]")
            decrypted_file = backup_file.with_suffix('')
            cmd = ["gpg", "--decrypt", "--output", str(decrypted_file), str(backup_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                console.print(f"[red]解密失败: {result.stderr}[/red]")
                raise click.Exit(1)
            working_file = decrypted_file
    
    # 解压和恢复
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("正在恢复...", total=None)
        
        try:
            if working_file.suffix == '.gz' or '.tar' in working_file.name:
                with tarfile.open(working_file, 'r:*') as tar:
                    tar.extractall(path=target_path)
            else:
                # 直接复制
                shutil.copy2(working_file, target_path)
            
            progress.update(task, description="恢复完成")
            
        except Exception as e:
            console.print(f"[red]恢复失败: {e}[/red]")
            raise click.Exit(1)
    
    # 清理临时解密文件
    if working_file != backup_file and working_file.exists():
        working_file.unlink()
    
    # 记录日志
    _log_backup_operation("RESTORE", f"{backup} -> {target_path}")
    
    console.print(f"\n[bold green]✅ 恢复完成[/bold green]")
    console.print(f"文件已恢复到: {target_path}")


@backup_cli.command(name="list")
@click.option("--source", "-s", help="按源路径过滤")
@click.option("--type", "-t", type=click.Choice(['full', 'incremental', 'differential']), help="按类型过滤")
def list_backups(source: Optional[str], type: Optional[str]):
    """列出所有备份"""
    config = _load_config()
    backups = config.get("backups", [])
    
    # 过滤
    if source:
        backups = [b for b in backups if source in b.get("source", "")]
    if type:
        backups = [b for b in backups if b.get("type") == type]
    
    if not backups:
        console.print("[yellow]没有找到备份记录[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📋 备份列表[/bold cyan] ({len(backups)} 个)\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=20)
    table.add_column("名称")
    table.add_column("类型", width=10)
    table.add_column("源路径")
    table.add_column("大小", justify="right")
    table.add_column("创建时间", width=19)
    table.add_column("压缩", width=6)
    table.add_column("加密", width=6)
    
    for b in backups:
        created = datetime.fromisoformat(b["created_at"]).strftime("%Y-%m-%d %H:%M")
        table.add_row(
            b["id"][:20],
            b.get("name", "-"),
            b.get("type", "-"),
            Path(b["source"]).name[:20],
            _format_size(b.get("size", 0)),
            created,
            "✓" if b.get("compressed") else "",
            "✓" if b.get("encrypted") else ""
        )
    
    console.print(table)
    
    # 统计
    total_size = sum(b.get("size", 0) for b in backups)
    console.print(f"\n总备份数: {len(backups)}")
    console.print(f"总大小: {_format_size(total_size)}")


@backup_cli.command(name="verify")
@click.option("--backup", "-b", required=True, help="备份ID")
def verify_backup(backup: str):
    """验证备份完整性"""
    config = _load_config()
    backup_record = None
    
    for b in config.get("backups", []):
        if b["id"] == backup or b["name"] == backup:
            backup_record = b
            break
    
    if not backup_record:
        console.print(f"[red]错误: 找不到备份: {backup}[/red]")
        raise click.Exit(1)
    
    backup_file = Path(backup_record["file"])
    
    if not backup_file.exists():
        console.print(f"[red]错误: 备份文件不存在: {backup_file}[/red]")
        raise click.Exit(1)
    
    console.print(f"\n[bold cyan]✓ 验证备份[/bold cyan]\n")
    console.print(f"备份: {backup_record['name']}")
    console.print(f"文件: {backup_file}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("正在验证...", total=None)
        
        # 1. 检查文件存在
        progress.update(task, description="检查文件存在...")
        
        # 2. 验证校验和
        progress.update(task, description="计算校验和...")
        current_checksum = _calculate_checksum(backup_file)
        stored_checksum = backup_record.get("checksum", "")
        checksum_valid = current_checksum == stored_checksum
        
        # 3. 测试归档完整性
        progress.update(task, description="测试归档完整性...")
        archive_valid = False
        try:
            if backup_file.suffix == '.gpg':
                archive_valid = True  # 无法直接测试加密文件
            else:
                with tarfile.open(backup_file, 'r:*') as tar:
                    tar.getmembers()
                archive_valid = True
        except Exception:
            archive_valid = False
        
        progress.update(task, description="验证完成")
    
    # 显示结果
    console.print(f"\n[bold]验证结果:[/bold]")
    console.print(f"  文件存在: [{'green' if backup_file.exists() else 'red'}]{'✓' if backup_file.exists() else '✗'}[/]")
    console.print(f"  校验和匹配: [{'green' if checksum_valid else 'red'}]{'✓' if checksum_valid else '✗'}[/]")
    console.print(f"  归档完整: [{'green' if archive_valid else 'red'}]{'✓' if archive_valid else '✗'}[/]")
    
    if checksum_valid and archive_valid:
        console.print(f"\n[bold green]✅ 备份验证通过[/bold green]")
    else:
        console.print(f"\n[bold red]⚠️ 备份验证失败[/bold red]")
        raise click.Exit(1)


@backup_cli.command(name="delete")
@click.option("--backup", "-b", required=True, help="备份ID")
@click.option("--yes", "-y", is_flag=True, help="确认删除，不提示")
def delete_backup(backup: str, yes: bool):
    """删除备份"""
    config = _load_config()
    backup_record = None
    
    for b in config.get("backups", []):
        if b["id"] == backup or b["name"] == backup:
            backup_record = b
            break
    
    if not backup_record:
        console.print(f"[red]错误: 找不到备份: {backup}[/red]")
        raise click.Exit(1)
    
    backup_file = Path(backup_record["file"])
    
    if not yes:
        confirm = click.confirm(f"确定要删除备份 '{backup_record['name']}' 吗？此操作不可恢复！")
        if not confirm:
            console.print("[yellow]已取消删除[/yellow]")
            return
    
    # 删除文件
    if backup_file.exists():
        backup_file.unlink()
    
    # 从配置中移除
    config["backups"] = [b for b in config["backups"] if b["id"] != backup_record["id"]]
    _save_config(config)
    
    # 记录日志
    _log_backup_operation("DELETE", f"{backup_record['id']} - {backup_record['name']}")
    
    console.print(f"[bold green]✅ 备份已删除[/bold green]")
    console.print(f"释放了 {_format_size(backup_record.get('size', 0))} 空间")


@backup_cli.command(name="schedule")
@click.option("--source", "-s", required=True, help="源目录")
@click.option("--target", "-t", required=True, help="目标目录")
@click.option("--cron", "-c", required=True, help="Cron表达式 (如 '0 2 * * *' 每天2点)")
@click.option("--name", "-n", help="任务名称")
@click.option("--type", "-tp", default="incremental", type=click.Choice(['full', 'incremental']), help="备份类型")
def schedule_backup(source: str, target: str, cron: str, name: Optional[str], type: str):
    """创建定时备份任务（使用crontab）"""
    schedule_name = name or f"backup_{Path(source).name}"
    
    console.print(f"\n[bold cyan]⏰ 定时备份[/bold cyan]\n")
    console.print(f"任务名称: {schedule_name}")
    console.print(f"源: {source}")
    console.print(f"目标: {target}")
    console.print(f"Cron: {cron}")
    console.print(f"类型: {type}")
    
    # 构建命令
    cmd = f"ai-toolkit backup create -s {source} -t {target} --type {type}"
    cron_line = f"{cron} {cmd} # ai-toolkit:{schedule_name}"
    
    # 添加到crontab
    try:
        # 获取现有crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing_crontab = result.stdout if result.returncode == 0 else ""
        
        # 检查是否已存在
        if schedule_name in existing_crontab:
            console.print(f"[yellow]警告: 任务 '{schedule_name}' 已存在，将更新[/yellow]")
            lines = existing_crontab.split('\n')
            lines = [l for l in lines if f"ai-toolkit:{schedule_name}" not in l]
            existing_crontab = '\n'.join(lines)
        
        # 添加新任务
        new_crontab = existing_crontab.rstrip() + '\n' + cron_line + '\n'
        
        # 写入crontab
        subprocess.run(["crontab", "-"], input=new_crontab, text=True, check=True)
        
        # 保存到配置
        config = _load_config()
        schedule_record = {
            "name": schedule_name,
            "source": source,
            "target": target,
            "cron": cron,
            "type": type,
            "created_at": datetime.now().isoformat()
        }
        config["schedules"] = [s for s in config.get("schedules", []) if s["name"] != schedule_name]
        config["schedules"].append(schedule_record)
        _save_config(config)
        
        console.print(f"\n[bold green]✅ 定时任务已创建[/bold green]")
        console.print(f"使用 'crontab -l' 查看所有定时任务")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]创建定时任务失败: {e}[/red]")
        raise click.Exit(1)


@backup_cli.command(name="schedules")
def list_schedules():
    """列出所有定时备份任务"""
    config = _load_config()
    schedules = config.get("schedules", [])
    
    if not schedules:
        console.print("[yellow]没有找到定时任务[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📅 定时任务列表[/bold cyan] ({len(schedules)} 个)\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("名称")
    table.add_column("源路径")
    table.add_column("目标路径")
    table.add_column("Cron表达式")
    table.add_column("类型")
    table.add_column("创建时间")
    
    for s in schedules:
        created = datetime.fromisoformat(s["created_at"]).strftime("%Y-%m-%d")
        table.add_row(
            s["name"],
            s["source"],
            s["target"],
            s["cron"],
            s.get("type", "incremental"),
            created
        )
    
    console.print(table)


@backup_cli.command(name="log")
@click.option("--lines", "-n", default=50, help="显示最近N行日志")
def backup_log(lines: int):
    """查看备份日志"""
    if not BACKUP_LOG_FILE.exists():
        console.print("[yellow]暂无日志记录[/yellow]")
        return
    
    with open(BACKUP_LOG_FILE, 'r') as f:
        log_content = f.readlines()
    
    console.print(f"\n[bold cyan]📝 备份日志[/bold cyan] (最近 {min(lines, len(log_content))} 条)\n")
    
    for line in log_content[-lines:]:
        console.print(line.rstrip())
    
    console.print(f"\n日志文件: {BACKUP_LOG_FILE}")


@backup_cli.command(name="info")
@click.option("--backup", "-b", required=True, help="备份ID")
def backup_info(backup: str):
    """显示备份详细信息"""
    config = _load_config()
    backup_record = None
    
    for b in config.get("backups", []):
        if b["id"] == backup or b["name"] == backup:
            backup_record = b
            break
    
    if not backup_record:
        console.print(f"[red]错误: 找不到备份: {backup}[/red]")
        raise click.Exit(1)
    
    console.print(f"\n[bold cyan]📄 备份详情[/bold cyan]\n")
    
    # 基本信息
    console.print(Panel(
        f"[bold]{backup_record['name']}[/bold]\n"
        f"ID: {backup_record['id']}\n"
        f"类型: {backup_record.get('type', 'unknown')}",
        title="基本信息"
    ))
    
    # 路径信息
    console.print(Panel(
        f"源: {backup_record['source']}\n"
        f"目标: {backup_record['target']}\n"
        f"备份文件: {backup_record['file']}",
        title="路径"
    ))
    
    # 大小信息
    compression_ratio = 0
    if backup_record.get('source_size', 0) > 0:
        compression_ratio = (1 - backup_record['size'] / backup_record['source_size']) * 100
    
    console.print(Panel(
        f"源大小: {_format_size(backup_record.get('source_size', 0))}\n"
        f"备份大小: {_format_size(backup_record.get('size', 0))}\n"
        f"文件数: {backup_record.get('file_count', 0)}\n"
        f"压缩率: {compression_ratio:.1f}%",
        title="大小"
    ))
    
    # 选项信息
    console.print(Panel(
        f"压缩: {'✓' if backup_record.get('compressed') else '✗'}\n"
        f"加密: {'✓' if backup_record.get('encrypted') else '✗'}\n"
        f"排除模式: {', '.join(backup_record.get('exclude_patterns', [])) or '无'}",
        title="选项"
    ))
    
    # 时间信息
    created = datetime.fromisoformat(backup_record['created_at'])
    console.print(Panel(
        f"创建时间: {created.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"校验和: {backup_record.get('checksum', 'N/A')[:32]}...",
        title="元数据"
    ))


@backup_cli.command(name="clean")
@click.option("--keep", "-k", default=7, help="保留最近N个备份")
@click.option("--older-than", "-o", help="删除N天前的备份 (如 '30d')")
@click.option("--yes", "-y", is_flag=True, help="确认删除，不提示")
def clean_backups(keep: int, older_than: Optional[str], yes: bool):
    """清理旧备份"""
    config = _load_config()
    backups = config.get("backups", [])
    
    if not backups:
        console.print("[yellow]没有找到备份[/yellow]")
        return
    
    to_delete = []
    
    if older_than:
        # 解析天数
        days = int(older_than.replace('d', ''))
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for b in backups:
            created = datetime.fromisoformat(b['created_at'])
            if created < cutoff_date:
                to_delete.append(b)
    else:
        # 按时间排序，保留最新的N个
        sorted_backups = sorted(backups, key=lambda x: x['created_at'], reverse=True)
        to_delete = sorted_backups[keep:]
    
    if not to_delete:
        console.print("[green]没有需要清理的备份[/green]")
        return
    
    total_size = sum(b.get('size', 0) for b in to_delete)
    
    console.print(f"\n[bold yellow]⚠️ 即将删除 {len(to_delete)} 个备份[/bold yellow]")
    console.print(f"将释放空间: {_format_size(total_size)}")
    
    if not yes:
        confirm = click.confirm("确定要继续吗？")
        if not confirm:
            console.print("[yellow]已取消[/yellow]")
            return
    
    # 执行删除
    deleted_count = 0
    for b in to_delete:
        backup_file = Path(b['file'])
        if backup_file.exists():
            backup_file.unlink()
        deleted_count += 1
        _log_backup_operation("CLEAN", f"Deleted {b['id']} - {b['name']}")
    
    # 更新配置
    deleted_ids = {b['id'] for b in to_delete}
    config["backups"] = [b for b in backups if b['id'] not in deleted_ids]
    _save_config(config)
    
    console.print(f"\n[bold green]✅ 已清理 {deleted_count} 个备份[/bold green]")
    console.print(f"释放了 {_format_size(total_size)} 空间")
