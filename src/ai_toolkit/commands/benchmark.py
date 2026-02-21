"""
性能测试命令
"""

import click
import json
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="benchmark")
def benchmark_cli():
    """模型性能测试"""
    pass


@benchmark_cli.command(name="run")
@click.option("--model", "-m", required=True, help="模型名称")
@click.option("--prompts", "-p", type=click.Path(exists=True), help="测试提示词文件 (JSON)")
@click.option("--iterations", "-i", type=int, default=3, help="每个提示词运行次数")
@click.option("--output", "-o", type=click.Path(), help="结果输出文件")
def run_benchmark(model: str, prompts: str, iterations: int, output: str = None):
    """运行性能测试"""
    config = get_config()

    if not prompts:
        # 使用默认测试提示词
        test_prompts = [
            "请介绍一下你自己",
            "用Python写一个快速排序算法",
            "解释什么是机器学习",
            "写一个关于春天的短诗",
            "如何制作一杯咖啡？",
        ]
    else:
        with open(prompts, "r", encoding="utf-8") as f:
            data = json.load(f)
            test_prompts = data.get("prompts", [])

    console.print(f"🧪 性能测试")
    console.print(f"🤖 模型: [cyan]{model}[/cyan]")
    console.print(f"📝 提示词数: [cyan]{len(test_prompts)}[/cyan]")
    console.print(f"🔄 迭代次数: [cyan]{iterations}[/cyan]\n")

    results = []
    import requests

    with console.status("[bold green]运行测试中...") as status:
        for i, prompt in enumerate(test_prompts, 1):
            console.print(f"\n[{i}/{len(test_prompts)}] {prompt[:50]}...")

            times = []
            tokens_per_second = []

            for j in range(iterations):
                start_time = time.time()

                try:
                    response = requests.post(
                        f"{config.ollama_base_url}/api/generate",
                        json={"model": model, "prompt": prompt, "stream": False},
                        timeout=config.ollama_timeout * 2,
                    )
                    response.raise_for_status()

                    data = response.json()
                    elapsed = time.time() - start_time

                    tokens = data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                    tps = tokens / elapsed if elapsed > 0 else 0

                    times.append(elapsed)
                    tokens_per_second.append(tps)

                    console.print(f"   迭代 {j+1}: {elapsed:.2f}s, {tps:.1f} tokens/s")

                except Exception as e:
                    console.print(f"   [red]错误: {e}[/red]")

            if times:
                avg_time = sum(times) / len(times)
                avg_tps = sum(tokens_per_second) / len(tokens_per_second)

                result = {
                    "prompt": prompt,
                    "avg_time": avg_time,
                    "avg_tps": avg_tps,
                    "iterations": iterations,
                }
                results.append(result)

    # 显示结果
    console.print("\n" + "=" * 60)
    console.print("[bold]测试结果[/bold]")
    console.print("=" * 60 + "\n")

    table = Table(show_header=True)
    table.add_column("提示词", style="cyan")
    table.add_column("平均时间", style="green")
    table.add_column("平均速度", style="yellow")

    for result in results:
        table.add_row(
            result["prompt"][:40] + "...",
            f"{result['avg_time']:.2f}s",
            f"{result['avg_tps']:.1f} t/s",
        )

    console.print(table)

    # 计算总体统计
    if results:
        total_avg_time = sum(r["avg_time"] for r in results) / len(results)
        total_avg_tps = sum(r["avg_tps"] for r in results) / len(results)

        console.print(
            Panel(
                f"[cyan]总平均时间:[/cyan] {total_avg_time:.2f}s\n[cyan]总平均速度:[/cyan] {total_avg_tps:.1f} tokens/s",
                title="📊 总体统计",
                border_style="cyan",
            )
        )

    # 保存结果
    if output:
        output_data = {
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "iterations": iterations,
            "results": results,
        }

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        console.print(f"\n✅ 结果已保存到: [cyan]{output}[/cyan]")


@benchmark_cli.command(name="compare")
@click.argument("models", nargs=-1, required=True)
@click.option("--prompt", "-p", default="请介绍一下你自己", help="测试提示词")
@click.option("--iterations", "-i", type=int, default=3, help="每个模型运行次数")
def compare_models(models: tuple, prompt: str, iterations: int):
    """对比多个模型的性能"""
    config = get_config()

    console.print(f"⚖️  模型对比测试")
    console.print(f"📝 提示词: [cyan]{prompt}[/cyan]")
    console.print(f"🔄 迭代次数: [cyan]{iterations}[/cyan]\n")

    results = {}
    import requests

    for model in models:
        console.print(f"测试模型: [cyan]{model}[/cyan]")

        times = []
        tokens_per_second = []

        for i in range(iterations):
            try:
                start_time = time.time()

                response = requests.post(
                    f"{config.ollama_base_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=config.ollama_timeout * 2,
                )
                response.raise_for_status()

                data = response.json()
                elapsed = time.time() - start_time

                tokens = data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                tps = tokens / elapsed if elapsed > 0 else 0

                times.append(elapsed)
                tokens_per_second.append(tps)

            except Exception as e:
                console.print(f"  [red]错误: {e}[/red]")

        if times:
            avg_time = sum(times) / len(times)
            avg_tps = sum(tokens_per_second) / len(tokens_per_second)
            results[model] = {"avg_time": avg_time, "avg_tps": avg_tps}

    # 显示对比结果
    console.print("\n" + "=" * 60)
    console.print("[bold]对比结果[/bold]")
    console.print("=" * 60 + "\n")

    table = Table(show_header=True)
    table.add_column("模型", style="cyan")
    table.add_column("平均时间", style="green")
    table.add_column("平均速度", style="yellow")
    table.add_column("排名", style="magenta")

    # 按速度排序
    sorted_models = sorted(results.items(), key=lambda x: x[1]["avg_tps"], reverse=True)

    for rank, (model, data) in enumerate(sorted_models, 1):
        table.add_row(
            model,
            f"{data['avg_time']:.2f}s",
            f"{data['avg_tps']:.1f} t/s",
            f"#{rank}",
        )

    console.print(table)

    if sorted_models:
        fastest = sorted_models[0]
        console.print(
            f"\n🏆 最快模型: [cyan]{fastest[0]}[/cyan] ({fastest[1]['avg_tps']:.1f} tokens/s)"
        )
