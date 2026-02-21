"""
进度条工具
"""

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn,
)
from rich.console import Console
from typing import Optional, Callable
import time


def get_progress(console: Optional[Console] = None):
    """
    获取标准进度条

    Args:
        console: Console 实例

    Returns:
        Progress 实例
    """
    if console is None:
        console = Console()

    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def get_download_progress(console: Optional[Console] = None):
    """
    获取下载进度条

    Args:
        console: Console 实例

    Returns:
        Progress 实例
    """
    if console is None:
        console = Console()

    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def track_progress(
    func: Callable,
    total: int,
    description: str = "处理中",
    console: Optional[Console] = None,
):
    """
    跟踪函数执行进度

    Args:
        func: 要执行的函数
        total: 总数量
        description: 描述
        console: Console 实例

    Returns:
        函数执行结果
    """
    if console is None:
        console = Console()

    with get_progress(console) as progress:
        task = progress.add_task(description, total=total)

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            progress.update(task, advance=1)
            return result

        return wrapper


class ProgressTracker:
    """进度跟踪器"""

    def __init__(self, total: int, description: str = "处理中"):
        """
        初始化进度跟踪器

        Args:
            total: 总数量
            description: 描述
        """
        self.total = total
        self.description = description
        self.current = 0
        self.start_time = time.time()
        self.console = Console()

    def update(self, advance: int = 1):
        """
        更新进度

        Args:
            advance: 前进的步数
        """
        self.current += advance
        self._print_progress()

    def _print_progress(self):
        """打印进度"""
        percent = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time

        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
        else:
            eta = 0

        self.console.print(
            f"\r{self.description}: {self.current}/{self.total} ({percent:.1f}%) "
            f"[耗时: {elapsed:.1f}s, 剩余: {eta:.1f}s]",
            end="",
        )

        if self.current >= self.total:
            self.console.print()  # 换行

    def finish(self):
        """完成"""
        self.current = self.total
        self._print_progress()


def progress_iterator(items, description: str = "处理中"):
    """
    带进度条的迭代器

    Args:
        items: 可迭代对象
        description: 描述

    Yields:
        项目
    """
    tracker = ProgressTracker(len(items), description)

    for item in items:
        yield item
        tracker.update()

    tracker.finish()
