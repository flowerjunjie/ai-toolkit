#!/usr/bin/env python3
"""
自动迭代监控和重启脚本
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

class AutoIterationMonitor:
    """自动迭代监控器"""
    
    def __init__(self):
        self.status_file = Path.home() / ".ai-toolkit" / "iteration-status.json"
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.project_dir = Path("/root/.openclaw/workspace/projects/ai-toolkit")
        
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
        except:
            pass
        return None
    
    def check_and_restart(self):
        """检查并重启"""
        status = self.get_status()
        
        # 检查最后提交时间
        last_commit = self.get_last_commit_time()
        
        if last_commit:
            elapsed = datetime.now() - last_commit
            minutes = elapsed.total_seconds() / 60
            
            print(f"\n🔍 检查: 上次提交是 {minutes:.1f} 分钟前")
            
            # 如果超过10分钟，立即重启
            if elapsed.total_seconds() > 600:  # 10分钟
                print(f"⚠️ 超过10分钟无提交！立即启动第{status['iteration_round']+1}轮！")
                self.start_next_round(status['iteration_round'] + 1)
                return True
            else:
                print(f"✅ 正常运行中，距离上次提交 {minutes:.1f} 分钟")
                return False
        else:
            print("⚠️ 未找到提交记录，启动第32轮！")
            self.start_next_round(32)
            return True
    
    def start_next_round(self, round_number):
        """启动下一轮"""
        print(f"\n🚀 启动第{round_number}轮迭代！")
        
        # 更新状态
        status = self.get_status()
        status["iteration_round"] = round_number
        status["last_check"] = datetime.now().isoformat()
        status["status"] = "running"
        self.save_status(status)
        
        # 这里可以添加实际的开发逻辑
        print(f"✅ 第{round_number}轮已启动")
        print(f"💡 提示: 这是监控脚本，实际开发需要手动执行")
        
        return round_number
    
    def run_forever(self):
        """永远运行"""
        print("🔥 自动监控器启动！")
        print("⏰ 检测间隔: 10分钟")
        print("🚀 无限循环模式")
        print("="*50)
        
        while True:
            try:
                # 检查并重启
                self.check_and_restart()
                
                # 等待10分钟
                print("\n💤 等待10分钟后再次检查...")
                print(f"下次检查: {(datetime.now() + timedelta(minutes=10)).strftime('%H:%M:%S')}")
                print("="*50)
                
                time.sleep(600)  # 10分钟
                
            except KeyboardInterrupt:
                print("\n⏸️ 监控器已停止")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")
                print("🔄 5秒后重试...")
                time.sleep(5)

if __name__ == "__main__":
    monitor = AutoIterationMonitor()
    
    # 立即检查一次
    print("🔍 立即检查状态...")
    monitor.check_and_restart()
    
    # 询问是否启动永久监控
    print("\n是否启动永久监控？(y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice == 'y':
            monitor.run_forever()
        else:
            print("\n✅ 监控器未启动，将仅在本次运行时检查")
    except:
        print("\n✅ 监控器未启动，将仅在本次运行时检查")
