#!/usr/bin/env python3
"""
自动迭代监控脚本 - 完全自动化版本
无需交互，适合cron定时任务
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
import os
import sys

class AutoIterationMonitor:
    """自动迭代监控器 - 完全自动化"""
    
    def __init__(self):
        self.status_file = Path.home() / ".ai-toolkit" / "iteration-status.json"
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.project_dir = Path("/root/.openclaw/workspace/projects/ai-toolkit")
        self.log_file = self.project_dir / "auto-iteration.log"
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        
    def get_status(self):
        """获取当前状态"""
        if self.status_file.exists():
            try:
                with open(self.status_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_check": None,
            "last_commit": None,
            "iteration_round": 31,
            "status": "running"
        }
    
    def save_status(self, status):
        """保存状态"""
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
    
    def get_last_commit_time(self):
        """获取最后提交时间"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                timestamp = int(result.stdout.strip())
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            self.log(f"❌ 获取Git提交时间失败: {e}")
        return None
    
    def check_and_report(self):
        """检查并汇报"""
        self.log("=" * 60)
        self.log("🔍 自动迭代监控检查")
        
        status = self.get_status()
        current_round = status.get("iteration_round", 31)
        
        # 检查最后提交时间
        last_commit = self.get_last_commit_time()
        
        if last_commit:
            elapsed = datetime.now() - last_commit
            minutes = elapsed.total_seconds() / 60
            
            self.log(f"📊 当前状态:")
            self.log(f"  迭代轮数: {current_round}")
            self.log(f"  上次提交: {minutes:.1f} 分钟前")
            self.log(f"  提交哈希: {status.get('commit_hash', 'unknown')[:8]}...")
            
            # 检查是否超时
            if elapsed.total_seconds() > 600:  # 10分钟
                self.log(f"⚠️ 警告: 超过10分钟无提交！")
                self.log(f"💡 建议: 立即启动第{current_round+1}轮迭代")
                self.log(f"📋 命令: cd /root/.openclaw/workspace/projects/ai-toolkit && git add -A && git commit -m \"第{current_round+1}轮迭代\" && git push")
                return "RESTART_NEEDED"
            else:
                self.log(f"✅ 正常: 距离上次提交 {minutes:.1f} 分钟 (< 10分钟)")
                self.log(f"💡 下次检查: {(datetime.now() + timedelta(minutes=10)).strftime('%H:%M:%S')}")
                return "OK"
        else:
            self.log(f"⚠️ 未找到Git提交记录")
            self.log(f"💡 建议: 初始化Git仓库")
            return "NO_COMMITS"
        
        # 更新检查时间
        status["last_check"] = datetime.now().isoformat()
        self.save_status(status)
        
        return "OK"
    
    def notify(self, message):
        """发送通知"""
        self.log(f"📢 通知: {message}")
        # 这里可以添加其他通知方式（如Telegram、邮件等）

def main():
    """主函数"""
    monitor = AutoIterationMonitor()
    
    # 执行检查并汇报
    result = monitor.check_and_report()
    
    # 输出到stdout（cron会捕获）
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {result}")
    print(f"详细日志: {monitor.log_file}")

if __name__ == "__main__":
    main()
