"""
任务调度器
"""

import schedule
import time
import threading
from pathlib import Path
from typing import Callable, Dict, Any, Optional
from datetime import datetime


class TaskScheduler:
    """任务调度器"""

    def __init__(self) -> None:
        """初始化任务调度器"""
        self.tasks: Dict[str, schedule.Job] = {}
        self.running: bool = False
        self.thread: Optional[threading.Thread] = None

    def add_task(
        self,
        name: str,
        func: Callable[..., None],
        interval: int,
        unit: str = "minutes",
    ) -> None:
        """
        添加定时任务

        Args:
            name: 任务名称
            func: 执行函数
            interval: 时间间隔
            unit: 时间单位 (seconds, minutes, hours, days)
        """
        if unit == "seconds":
            job = schedule.every(interval).seconds.do(func)
        elif unit == "minutes":
            job = schedule.every(interval).minutes.do(func)
        elif unit == "hours":
            job = schedule.every(interval).hours.do(func)
        elif unit == "days":
            job = schedule.every(interval).days.do(func)
        else:
            raise ValueError(f"未知的时间单位: {unit}")

        self.tasks[name] = job

    def remove_task(self, name: str) -> None:
        """
        移除任务

        Args:
            name: 任务名称
        """
        if name in self.tasks:
            schedule.cancel_job(self.tasks[name])
            del self.tasks[name]

    def list_tasks(self) -> Dict[str, str]:
        """
        列出所有任务

        Returns:
            任务字典
        """
        return {
            name: str(job.job_type)
            for name, job in self.tasks.items()
        }

    def run_scheduler(self) -> None:
        """运行调度器"""
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def start(self) -> None:
        """启动调度器（后台线程）"""
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

    def run_once(self) -> None:
        """运行一次所有待执行的任务"""
        schedule.run_pending()


# 全局调度器
_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """获取全局调度器"""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler()
    return _scheduler
