"""
错误处理和用户友好的错误消息
"""

from typing import Optional, Dict, Any
from rich.console import Console


class ToolkitError(Exception):
    """AI Toolkit 基础异常"""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        """
        初始化异常

        Args:
            message: 错误消息
            suggestion: 解决建议
        """
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)


class OllamaConnectionError(ToolkitError):
    """Ollama 连接错误"""

    def __init__(self):
        super().__init__(
            "无法连接到 Ollama 服务",
            "请确保 Ollama 正在运行: ollama serve\n安装: https://ollama.ai"
        )


class ModelNotFoundError(ToolkitError):
    """模型未找到错误"""

    def __init__(self, model_name: str):
        super().__init__(
            f"模型未找到: {model_name}",
            f"使用 'ai-toolkit models pull {model_name}' 下载模型\n"
            f"或使用 'ai-toolkit models list' 查看可用模型"
        )


class PromptNotFoundError(ToolkitError):
    """Prompt 未找到错误"""

    def __init__(self, prompt_name: str):
        super().__init__(
            f"Prompt 模板未找到: {prompt_name}",
            f"使用 'ai-toolkit prompts list' 查看可用模板\n"
            f"或使用 'ai-toolkit prompts add {prompt_name} \"你的内容\"' 创建"
        )


class RAGNotFoundError(ToolkitError):
    """RAG 知识库未找到错误"""

    def __init__(self, rag_name: str):
        super().__init__(
            f"RAG 知识库未找到: {rag_name}",
            f"使用 'ai-toolkit rag2 list' 查看可用知识库\n"
            f"或使用 'ai-toolkit rag2 create <path> --name {rag_name}' 创建"
        )


class ConfigurationError(ToolkitError):
    """配置错误"""

    def __init__(self, message: str, suggestion: Optional[str] = None):
        if suggestion is None:
            suggestion = "使用 'ai-toolkit config reset' 重置配置"
        super().__init__(message, suggestion)


class APIKeyError(ToolkitError):
    """API Key 错误"""

    def __init__(self, provider: str):
        super().__init__(
            f"{provider} 的所有 API Key 都不可用",
            "请检查 API Key 配置\n"
            "使用 'ai-toolkit coding status' 查看状态"
        )


def handle_error(error: Exception, console: Optional[Console] = None) -> None:
    """
    处理错误并显示友好的错误消息

    Args:
        error: 异常对象
        console: Console 实例
    """
    if console is None:
        console = Console()

    if isinstance(error, ToolkitError):
        # 自定义错误
        console.print(f"\n[red]❌ {error.message}[/red]\n")

        if error.suggestion:
            console.print(f"[dim]💡 建议:[/dim]")
            console.print(f"[dim]{error.suggestion}[/dim]\n")

    elif isinstance(error, ConnectionError):
        console.print("\n[red]❌ 网络连接错误[/red]\n")
        console.print("[dim]💡 请检查网络连接[/dim]\n")

    elif isinstance(error, FileNotFoundError):
        console.print(f"\n[red]❌ 文件未找到: {error.filename}[/red]\n")

    elif isinstance(error, PermissionError):
        console.print("\n[red]❌ 权限不足[/red]\n")
        console.print("[dim]💡 请检查文件权限[/dim]\n")

    elif isinstance(error, KeyboardInterrupt):
        console.print("\n[yellow]⚠️  操作已取消[/yellow]\n")

    else:
        # 其他错误
        console.print(f"\n[red]❌ 错误: {str(error)}[/red]\n")
        console.print("[dim]💡 如果问题持续存在，请提交 issue:[/dim]")
        console.print("[dim]https://github.com/flowerjunjie/ai-toolkit/issues\n")


def safe_execute(func, *args, **kwargs):
    """
    安全执行函数，捕获并处理错误

    Args:
        func: 要执行的函数
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        函数执行结果，或 None（如果出错）
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e)
        return None
