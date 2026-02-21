"""
助手函数和实用工具
"""

import os
import sys
import time
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import requests


console = Console()


class OllamaConnectionError(Exception):
    """Ollama 连接错误"""
    pass


class ModelNotFoundError(Exception):
    """模型未找到错误"""
    pass


def check_ollama_connection(base_url: str = "http://localhost:11434", timeout: int = 5) -> bool:
    """
    检查 Ollama 是否可用

    Args:
        base_url: Ollama 服务地址
        timeout: 超时时间

    Returns:
        bool: 是否可用
    """
    try:
        response = requests.get(f"{base_url}", timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def ensure_ollama_running(base_url: str = "http://localhost:11434") -> None:
    """
    确保 Ollama 正在运行，否则抛出错误

    Args:
        base_url: Ollama 服务地址

    Raises:
        OllamaConnectionError: Ollama 不可用
    """
    if not check_ollama_connection(base_url):
        raise OllamaConnectionError(
            f"无法连接到 Ollama 服务 ({base_url})\n"
            f"请确保 Ollama 正在运行。\n"
            f"安装: https://ollama.ai\n"
            f"启动: ollama serve"
        )


def download_with_progress(url: str, dest_path: Path, description: str = "下载中") -> None:
    """
    带进度条的下载

    Args:
        url: 下载地址
        dest_path: 目标路径
        description: 进度描述
    """
    import requests

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(description, total=None)

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            progress.update(task, total=total_size)

            downloaded = 0
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress.update(task, completed=downloaded)

            console.print(f"✅ 下载完成: {dest_path.name}")

        except Exception as e:
            console.print(f"[red]下载失败: {e}[/red]")
            raise


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    加载 JSON 文件

    Args:
        file_path: 文件路径

    Returns:
        解析后的字典
    """
    if not file_path.exists():
        return {}

    try:
        import json

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]读取文件失败 {file_path}: {e}[/red]")
        return {}


def save_json_file(file_path: Path, data: Dict[str, Any]) -> bool:
    """
    保存 JSON 文件

    Args:
        file_path: 文件路径
        data: 要保存的数据

    Returns:
        是否成功
    """
    try:
        import json

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        console.print(f"[red]保存文件失败 {file_path}: {e}[/red]")
        return False


def get_file_size(file_path: Path) -> int:
    """
    获取文件大小

    Args:
        file_path: 文件路径

    Returns:
        文件大小（字节）
    """
    try:
        return file_path.stat().st_size
    except FileNotFoundError:
        return 0


def get_directory_size(dir_path: Path) -> int:
    """
    获取目录大小

    Args:
        dir_path: 目录路径

    Returns:
        目录大小（字节）
    """
    total_size = 0
    try:
        for item in dir_path.rglob("*"):
            if item.is_file():
                total_size += item.stat().st_size
    except FileNotFoundError:
        pass
    return total_size


def find_files_by_extension(directory: Path, extensions: List[str]) -> List[Path]:
    """
    按扩展名查找文件

    Args:
        directory: 搜索目录
        extensions: 扩展名列表（如 [".txt", ".md"]）

    Returns:
        文件路径列表
    """
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f"*{ext}"))
    return files


def safe_delete(path: Path) -> bool:
    """
    安全删除文件或目录

    Args:
        path: 文件或目录路径

    Returns:
        是否成功
    """
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return True
    except Exception as e:
        console.print(f"[red]删除失败 {path}: {e}[/red]")
        return False


def create_backup(path: Path, suffix: str = ".backup") -> Optional[Path]:
    """
    创建文件备份

    Args:
        path: 原文件路径
        suffix: 备份文件后缀

    Returns:
        备份文件路径，失败返回 None
    """
    if not path.exists():
        return None

    backup_path = path.with_suffix(path.suffix + suffix)

    try:
        if path.is_file():
            shutil.copy2(path, backup_path)
        elif path.is_dir():
            shutil.copytree(path, backup_path)
        return backup_path
    except Exception as e:
        console.print(f"[red]备份失败 {path}: {e}[/red]")
        return None


def confirm_deletion(items: List[Any], item_type: str = "项") -> bool:
    """
    确认删除操作

    Args:
        items: 要删除的项目列表
        item_type: 项目类型名称

    Returns:
        是否确认删除
    """
    if not items:
        return False

    console.print(f"[yellow]即将删除 {len(items)} 个{item_type}[/yellow]")

    try:
        response = input("确定要删除吗？[y/N]: ").strip().lower()
        return response in ["y", "yes"]
    except (EOFError, KeyboardInterrupt):
        return False


def retry_on_failure(func, max_retries: int = 3, delay: float = 1.0, *args, **kwargs):
    """
    失败重试装饰器

    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        delay: 重试延迟（秒）
        *args: 函数参数
        **kwargs: 函数关键字参数

    Returns:
        函数执行结果
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                console.print(f"[yellow]重试 {attempt + 1}/{max_retries}...[/yellow]")
                time.sleep(delay)

    raise last_error


def get_editor() -> Optional[str]:
    """
    获取用户编辑器

    Returns:
        编辑器路径
    """
    return os.environ.get("EDITOR") or os.environ.get("VISUAL") or None


def open_in_editor(file_path: Path) -> bool:
    """
    在编辑器中打开文件

    Args:
        file_path: 文件路径

    Returns:
        是否成功
    """
    editor = get_editor()
    if not editor:
        console.print("[yellow]未配置编辑器 (设置 EDITOR 环境变量)[/yellow]")
        return False

    try:
        os.system(f"{editor} {file_path}")
        return True
    except Exception as e:
        console.print(f"[red]打开编辑器失败: {e}[/red]")
        return False
