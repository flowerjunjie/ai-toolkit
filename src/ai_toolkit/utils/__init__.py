"""
工具函数
"""

import sys
from pathlib import Path
from typing import Optional


def check_ollama_running(base_url: str = "http://localhost:11434") -> bool:
    """检查 Ollama 是否运行"""
    try:
        import requests

        response = requests.get(f"{base_url}", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def confirm_action(prompt: str, default: bool = False) -> bool:
    """确认操作"""
    if default:
        prompt = f"{prompt} [Y/n]: "
    else:
        prompt = f"{prompt} [y/N]: "

    try:
        response = input(prompt).strip().lower()
        if not response:
            return default
        return response in ["y", "yes"]
    except (EOFError, KeyboardInterrupt):
        return False


def validate_model_name(name: str) -> bool:
    """验证模型名称格式"""
    if not name:
        return False
    return len(name) > 0 and all(c.isalnum() or c in "._-" for c in name)


def sanitize_filename(name: str) -> str:
    """清理文件名"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "_")
    return name.strip()


def get_editor() -> Optional[str]:
    """获取用户编辑器"""
    return os.environ.get("EDITOR") or os.environ.get("VISUAL")


def open_file_in_editor(filepath: Path) -> bool:
    """在编辑器中打开文件"""
    editor = get_editor()
    if editor:
        import os

        try:
            os.system(f"{editor} {filepath}")
            return True
        except Exception:
            return False
    return False


def print_success(message: str):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message: str):
    """打印错误消息"""
    print(f"❌ {message}")


def print_warning(message: str):
    """打印警告消息"""
    print(f"⚠️  {message}")


def print_info(message: str):
    """打印信息消息"""
    print(f"ℹ️  {message}")


import os
