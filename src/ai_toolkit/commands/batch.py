"""
批处理命令
"""

import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

console = Console()


@click.command()
@click.argument("batch_file", type=click.Path(exists=True))
@click.option("--parallel", "-p", is_flag=True, help="并行执行")
@click.option("--continue-on-error", "-c", is_flag=True, help="出错时继续")
def batch(batch_file: str, parallel: bool, continue_on_error: bool):
    """批量执行命令"""
    import subprocess

    batch_path = Path(batch_file)

    with open(batch_path, "r", encoding="utf-8") as f:
        commands = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    console.print(f"📦 批处理模式")
    console.print(f"文件: {batch_path}")
    console.print(f"命令数: {len(commands)}")
    console.print(f"并行: {'是' if parallel else '否'}")
    console.print(f"错误继续: {'是' if continue_on_error else '否'}\n")

    results = []

    with Progress() as progress:
        task = progress.add_task("执行命令...", total=len(commands))

        for i, cmd in enumerate(commands, 1):
            try:
                console.print(f"\n[{i}/{len(commands)}] $ {cmd}")

                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    console.print(f"[green]✅ 成功[/green]")
                    if result.stdout:
                        console.print(f"[dim]{result.stdout[:200]}[/dim]")
                    results.append({"command": cmd, "status": "success"})
                else:
                    console.print(f"[red]❌ 失败[/red]")
                    if result.stderr:
                        console.print(f"[dim]{result.stderr[:200]}[/dim]")
                    results.append({"command": cmd, "status": "failed", "error": result.stderr})

                    if not continue_on_error:
                        console.print("\n[yellow]批处理已中止[/yellow]")
                        break

            except Exception as e:
                console.print(f"[red]❌ 异常: {e}[/red]")
                results.append({"command": cmd, "status": "error", "error": str(e)})

                if not continue_on_error:
                    console.print("\n[yellow]批处理已中止[/yellow]")
                    break

            progress.update(task, advance=1)

    # 统计
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count

    console.print(f"\n📊 统计:")
    console.print(f"   成功: [green]{success_count}[/green]")
    console.print(f"   失败: [red]{failed_count}[/red]")
    console.print(f"   总计: {len(results)}")
