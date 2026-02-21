"""
RAG（检索增强生成）命令
"""

import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

from ai_toolkit.core.config import get_config

console = Console()


@click.group(name="rag")
def rag_cli():
    """RAG（检索增强生成）知识库管理"""
    pass


@rag_cli.command(name="create")
@click.argument("docs_path", type=click.Path(exists=True))
@click.option("--name", "-n", default="default", help="知识库名称")
@click.option("--chunk-size", type=int, default=1000, help="文本块大小")
@click.option("--chunk-overlap", type=int, default=200, help="文本块重叠")
def create_rag(docs_path: str, name: str, chunk_size: int, chunk_overlap: int):
    """创建RAG知识库"""
    config = get_config()

    docs_path = Path(docs_path)
    if not docs_path.exists():
        console.print(f"[red]文档路径不存在: {docs_path}[/red]")
        return

    rag_db_dir = config.rag_dir / name
    rag_db_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"📚 创建知识库: [cyan]{name}[/cyan]")
    console.print(f"📁 文档路径: {docs_path}")
    console.print(f"📦 知识库目录: {rag_db_dir}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在扫描文档...", total=None)

        # 扫描文档文件
        doc_files = []
        for ext in [".txt", ".md", ".pdf", ".docx", ".html"]:
            doc_files.extend(docs_path.rglob(f"*{ext}"))

        if not doc_files:
            console.print("[yellow]未找到支持的文档文件[/yellow]")
            console.print("支持的格式: .txt, .md, .pdf, .docx, .html")
            return

        progress.update(task, description=f"找到 {len(doc_files)} 个文件")

        # 保存元数据
        metadata = {
            "name": name,
            "docs_path": str(docs_path),
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "files": [str(f.relative_to(docs_path)) for f in doc_files],
            "created_at": str(pd_timestamp()),
        }

        metadata_file = rag_db_dir / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    console.print(f"\n✅ 知识库 [cyan]{name}[/cyan] 创建完成!")
    console.print(f"   索引了 [cyan]{len(doc_files)}[/cyan] 个文件")
    console.print(f"\n使用以下命令查询:")
    console.print(f"   [cyan]ai-toolkit rag query {name} \"你的问题\"[/cyan]")


@rag_cli.command(name="query")
@click.argument("name")
@click.argument("question")
@click.option("--top-k", type=int, default=3, help="返回前K个相关片段")
def query_rag(name: str, question: str, top_k: int):
    """查询RAG知识库"""
    config = get_config()

    rag_db_dir = config.rag_dir / name
    if not rag_db_dir.exists():
        console.print(f"[red]知识库不存在: {name}[/red]")
        console.print("使用 [cyan]ai-toolkit rag create <docs_path>[/cyan] 创建知识库")
        return

    metadata_file = rag_db_dir / "metadata.json"
    if not metadata_file.exists():
        console.print(f"[red]知识库元数据丢失: {name}[/red]")
        return

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    console.print(f"🔍 查询知识库: [cyan]{name}[/cyan]")
    console.print(f"❓ 问题: {question}\n")

    # 简单的关键词匹配（实际应该用向量检索）
    console.print("[dim]提示: 完整的RAG功能需要安装额外依赖[/dim]")
    console.print("[dim]安装: pip install ai-toolkit[rag][/dim]\n")

    console.print("[yellow]当前使用简单关键词匹配[/yellow]")

    docs_path = Path(metadata["docs_path"])
    results = []

    for file_path in metadata.get("files", []):
        full_path = docs_path / file_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # 简单的关键词匹配
                keywords = question.split()
                score = sum(1 for kw in keywords if kw.lower() in content.lower())
                if score > 0:
                    results.append({"file": file_path, "score": score, "content": content[:500]})
            except Exception as e:
                pass

    # 按相关性排序
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top_k]

    if not results:
        console.print("[yellow]未找到相关内容[/yellow]")
        return

    from rich.panel import Panel

    for i, result in enumerate(results, 1):
        console.print(
            Panel(
                f"[cyan]文件:[/cyan] {result['file']}\n[cyan]相关度:[/cyan] {result['score']}\n\n[dim]{result['content']}...[/dim]",
                title=f"结果 {i}",
                border_style="cyan",
            )
        )
        console.print()


@rag_cli.command(name="list")
def list_rag():
    """列出所有知识库"""
    config = get_config()

    if not config.rag_dir.exists():
        console.print("[yellow]暂无知识库[/yellow]")
        return

    rag_dbs = [d for d in config.rag_dir.iterdir() if d.is_dir() and (d / "metadata.json").exists()]

    if not rag_dbs:
        console.print("[yellow]暂无知识库[/yellow]")
        return

    from rich.table import Table

    table = Table(title="📚 RAG知识库", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("文件数", style="green")
    table.add_column("Chunk大小", style="yellow")
    table.add_column("文档路径", style="blue")

    for rag_db in rag_dbs:
        metadata_file = rag_db / "metadata.json"
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        name = metadata.get("name", rag_db.name)
        files_count = len(metadata.get("files", []))
        chunk_size = metadata.get("chunk_size", "N/A")
        docs_path = metadata.get("docs_path", "N/A")

        table.add_row(name, str(files_count), str(chunk_size), docs_path[:50])

    console.print(table)


@rag_cli.command(name="delete")
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="强制删除")
def delete_rag(name: str, force: bool):
    """删除知识库"""
    if not force:
        if not click.confirm(f"确定要删除知识库 '{name}' 吗？"):
            console.print("已取消")
            return

    config = get_config()
    rag_db_dir = config.rag_dir / name

    if not rag_db_dir.exists():
        console.print(f"[red]知识库不存在: {name}[/red]")
        return

    import shutil

    shutil.rmtree(rag_db_dir)
    console.print(f"✅ 知识库 [cyan]{name}[/cyan] 已删除")


def pd_timestamp():
    """获取当前时间戳"""
    from datetime import datetime

    return datetime.now().isoformat()
