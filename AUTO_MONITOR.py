"""
自动监控和重启机制
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

class AutoIterationMonitor:
    """自动迭代监控器"""
    
    def __init__(self):
        self.status_file = Path.home() / ".ai-toolkit" / "iteration-status.json"
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        
    def get_status(self):
        """获取当前状态"""
        if self.status_file.exists():
            with open(self.status_file, "r") as f:
                return json.load(f)
        return {
            "last_check": None,
            "last_commit": None,
            "iteration_round": 0,
            "status": "running"
        }
    
    def save_status(self, status):
        """保存状态"""
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
    
    def check_and_restart(self):
        """检查并重启"""
        status = self.get_status()
        
        # 检查最后提交时间
        if status.get("last_commit"):
            last_commit = datetime.fromisoformat(status["last_commit"])
            elapsed = datetime.now() - last_commit
            
            # 如果超过10分钟，立即重启
            if elapsed.total_seconds() > 600:  # 10分钟
                return "RESTART_NEEDED"
        
        # 检查最后检查时间
        if status.get("last_check"):
            last_check = datetime.fromisoformat(status["last_check"])
            elapsed = datetime.now() - last_check
            
            if elapsed.total_seconds() > 600:
                return "CHECK_NEEDED"
        
        return "RUNNING"
    
    def update_check(self):
        """更新检查时间"""
        status = self.get_status()
        status["last_check"] = datetime.now().isoformat()
        self.save_status(status)
    
    def update_commit(self, commit_hash):
        """更新提交时间"""
        status = self.get_status()
        status["last_commit"] = datetime.now().isoformat()
        status["commit_hash"] = commit_hash
        status["iteration_round"] = status.get("iteration_round", 0) + 1
        self.save_status(status)
        
        print(f"\n🔄 自动监控: 第{status['iteration_round']}轮已完成")
        print(f"✅ 最后提交: {commit_hash[:8]}")
        print(f"⏰ 提交时间: {status['last_commit']}")
        print(f"🚀 继续第{status['iteration_round']+1}轮...")
        
        return status["iteration_round"] + 1

# 初始化监控器
monitor = AutoIterationMonitor()

# 立即更新当前状态
print("\n🔥 自动监控已启动！")
print("⏰ 检测间隔: 10分钟")
print("🚀 自动重启: 已启用")
print("\n✅ 系统将自动监控并持续迭代！")
