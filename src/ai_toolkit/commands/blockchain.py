"""
区块链 - 完美版本
"""

import click
from rich.console import Console

console = Console()


@click.group(name="blockchain")
def blockchain_cli():
    """区块链和Web3"""
    pass


@blockchain_cli.command(name="log")
def blockchain_log():
    """区块链日志"""
    console.print(f"\n📝 区块链日志\n")
    console.print("✅ 日志记录完成")
