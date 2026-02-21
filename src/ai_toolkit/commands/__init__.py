"""
命令模块
"""

from ai_toolkit.commands.models import models_cli
from ai_toolkit.commands.prompts import prompts_cli
from ai_toolkit.commands.rag import rag_cli
from ai_toolkit.commands.benchmark import benchmark_cli

__all__ = [
    "models_cli",
    "prompts_cli",
    "rag_cli",
    "benchmark_cli",
]
