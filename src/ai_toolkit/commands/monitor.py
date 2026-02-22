"""
系统监控命令
"""

import click
import psutil
import shutil
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import time

console = Console()


@click.group(name="monitor")
def monitor_cli():
    """系统监控"""
    pass


@monitor_cli.command(name="status")
def monitor_status():
    """显示系统状态"""
    console.print("\n📊 系统状态\n")

    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    console.print(f"CPU使用率: [cyan]{cpu_percent}%[/cyan]")

    # 内存
    memory = psutil.virtual_memory()
    console.print(f"内存使用: [cyan]{memory.percent}%[/cyan] ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)")

    # 磁盘
    disk = psutil.disk_usage("/")
    console.print(f"磁盘使用: [cyan]{disk.percent}%[/cyan] ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")

    # 网络
    net_io = psutil.net_io_counters()
    console.print(f"网络发送: [cyan]{net_io.bytes_sent // 1024 / 1024}MB[/cyan]")
    console.print(f"网络接收: [cyan]{net_io.bytes_recv // 1024 / 1024}MB[/cyan]")

    # 进程
    process = psutil.Process()
    console.print(f"\n当前进程:")
    console.print(f"  PID: [cyan]{process.pid}[/cyan]")
    console.print(f"  内存: [cyan]{process.memory_info().rss // 1024 / 1024}MB[/cyan]")
    console.print(f"  线程: [cyan]{process.num_threads()}[/cyan]")
    console.print(f"  文件描述符: [cyan]{process.num_fds()}[/cyan]")


@monitor_cli.command(name="top")
@click.option("--interval", "-i", default=1, help="刷新间隔（秒）")
@click.option("--lines", "-n", default=20, help="显示行数")
def monitor_top(interval: int, lines: int):
    """实时监控（类似top）"""
    console.print(f"🔍 实时监控 (每{interval}秒刷新)")
    console.print("按 Ctrl+C 停止\n")

    try:
        while True:
            console.clear()

            # 显示标题
            console.print(f"[bold]AI Toolkit 监控[/bold] - {time.strftime('%H:%M:%S')}")
            console.print("")

            # CPU和内存
            cpu = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()

            table = Table(show_header=True)
            table.add_column("指标", style="cyan")
            table.add_column("值", style="green")
            table.add_column("说明", style="yellow")

            table.add_row("CPU使用率", f"{cpu}%", f"{'高' if cpu > 80 else '正常'}")
            table.add_row("内存使用率", f"{memory.percent}%", f"{memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB")
            table.add_row("可用内存", f"{memory.available // 1024 // 1024}MB", "")

            # 磁盘
            disk = psutil.disk_usage("/")
            table.add_row("磁盘使用率", f"{disk.percent}%", f"{disk.free // 1024 // 1024}GB 可用")

            console.print(table)

            # 进程信息
            process = psutil.Process()
            console.print(f"\n当前进程:")
            console.print(f"  PID: {process.pid}")
            console.print(f"  CPU: {process.cpu_percent()}%")
            console.print(f"  内存: {process.memory_info().rss // 1024 / 1024}MB")
            console.print(f"  线程: {process.num_threads()}")

            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n[yellow]监控已停止[/yellow]")


@monitor_cli.command(name="health")
@click.option("--verbose", "-v", is_flag=True, help="详细信息")
def health_check(verbose: bool):
    """健康检查"""
    console.print("\n🏥 系统健康检查\n")

    checks = []

    # 检查 Python 版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 8):
        console.print(f"✅ Python版本: {python_version}")
    else:
        console.print(f"❌ Python版本过低: {python_version}")
        checks.append(False)

    # 检查磁盘空间
    disk = psutil.disk_usage("/")
    if disk.free > 1 * 1024**3:  # 大于1GB
        console.print(f"✅ 磁盘空间: {disk.free // 1024 // 1024}GB 可用")
    else:
        console.print(f"⚠️  磁盘空间不足: {disk.free // 1024 // 1024}GB")
        checks.append(False)

    # 检查内存
    memory = psutil.virtual_memory()
    if memory.available > 512 * 1024 * 1024:  # 大于512MB
        console.print(f"✅ 可用内存: {memory.available // 1024 // 1024}MB")
    else:
        console.print(f"⚠️  可用内存不足: {memory.available // 1024 // 1024}MB")
        checks.append(False)

    # 检查配置
    from ai_toolkit.core.config import get_config
    try:
        config = get_config()
        console.print(f"✅ 配置文件: {config.config_path}")
    except Exception as e:
        console.print(f"❌ 配置加载失败: {e}")
        checks.append(False)

    if verbose:
        console.print(f"\n详细检查:")

        # 检查Ollama
        try:
            from ai_toolkit.core.api_manager import get_api_manager
            api_manager = get_api_manager()
            console.print(f"✅ API Keys: {api_manager.get_available_count()}/{api_manager.get_total_count()} 可用")
        except Exception as e:
            console.print(f"❌ API检查失败: {e}")

    # 总结
    console.print(f"\n{'='*60}")
    if not checks:
        console.print("[green]✅ 系统健康！[/green]")
    else:
        console.print(f"[yellow]⚠️  发现 {len(checks)} 个问题[/yellow]")


def import_sys():
    import sys
    return sys
