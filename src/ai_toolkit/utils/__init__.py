"""
工具函数
"""

# 导入错误处理相关
from ai_toolkit.utils.errors import (
    APIKeyError,
    ConfigurationError,
    ModelNotFoundError,
    OllamaConnectionError,
    PromptNotFoundError,
    RAGNotFoundError,
    ToolkitError,
    handle_error,
    safe_execute,
)

# 导入所有公开的工具函数
from ai_toolkit.utils.helpers import (
    check_ollama_connection,
    format_duration,
    format_size,
    get_editor,
    open_file_in_editor,
    print_error,
    print_info,
    print_success,
    print_warning,
    sanitize_filename,
    validate_model_name,
)

# 导入日志相关
from ai_toolkit.utils.logger import LoggerMixin, get_logger, setup_logger

# 导入进度条相关
from ai_toolkit.utils.progress import (
    ProgressTracker,
    get_download_progress,
    get_progress,
    progress_iterator,
)

__all__ = [
    # helpers
    "check_ollama_connection",
    "format_size",
    "format_duration",
    "validate_model_name",
    "sanitize_filename",
    "get_editor",
    "open_file_in_editor",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    # logger
    "setup_logger",
    "get_logger",
    "LoggerMixin",
    # progress
    "get_progress",
    "get_download_progress",
    "ProgressTracker",
    "progress_iterator",
    # errors
    "ToolkitError",
    "OllamaConnectionError",
    "ModelNotFoundError",
    "PromptNotFoundError",
    "RAGNotFoundError",
    "ConfigurationError",
    "APIKeyError",
    "handle_error",
    "safe_execute",
]
