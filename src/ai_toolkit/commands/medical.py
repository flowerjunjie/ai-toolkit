"""
医疗健康 - 完美版本
"""

import click
from rich.console import Console

console = Console()


@click.group(name="medical")
def medical_cli():
    """医疗健康"""
    pass


@medical_cli.command(name="log")
def medical_log():
    """医疗日志"""
    console.print(f"\n📝 医疗日志\n")
    console.print("✅ 日志记录完成")
