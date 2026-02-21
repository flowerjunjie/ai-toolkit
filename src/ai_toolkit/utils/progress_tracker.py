"""
进度追踪器 - 实时记录开发进度
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class ProgressTracker:
    """进度追踪器"""

    def __init__(self):
        """初始化追踪器"""
        self.progress_file = Path.home() / ".ai-toolkit" / "progress.json"
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """加载进度数据"""
        if self.progress_file.exists():
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "rounds_completed": 0,
            "total_commits": 0,
            "features_added": 0,
            "bugs_fixed": 0,
            "hours_worked": 0,
            "last_update": None,
            "changes": [],
        }

    def _save(self):
        """保存进度数据"""
        self.data["last_update"] = datetime.now().isoformat()

        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add_round(
        self,
        round_number: int,
        features: int,
        commits: int,
        changes: List[str],
    ):
        """添加一轮迭代"""
        self.data["rounds_completed"] = round_number
        self.data["features_added"] += features
        self.data["total_commits"] += commits
        self.data["changes"].extend(changes)

        self._save()

    def add_fix(self, bug_description: str):
        """记录修复的bug"""
        if "bugs_fixed" not in self.data:
            self.data["bugs_fixed"] = 0

        self.data["bugs_fixed"] += 1
        self.data["changes.append(f"修复: {bug_description}")

        self._save()

    def add_feature(self, feature: str):
        """记录新增功能"""
        self.data["features_added"] += 1
        self.data["changes"].append(f"新增: {feature}")

        self._save()

    def add_hour(self):
        """记录工作一小时"""
        if "hours_worked" not in self.data:
            self.data["hours_worked"] = 0

        self.data["hours_worked"] += 1
        self._save()

    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return self.data


# 全局追踪器
_tracker: ProgressTracker = None


def get_progress_tracker() -> ProgressTracker:
    """获取进度追踪器"""
    global _tracker
    if _tracker is None:
        _tracker = ProgressTracker()
    return _tracker
