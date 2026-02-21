"""
RAG 命令 v2 - 真正的向量检索版本
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import json

from ai_toolkit.core.config import get_config
from ai_toolkit.core.vector_store import VectorStore
from ai_toolkit.core.document_loader import DocumentLoader

console = Console()


@click.group(name="rag2")
def rag2_cli():
    """RAG 向量检索（v2 - 实验性）"""
    pass


@rag2_cli.command(name="create")
@click.argument("docs_path", type=click.Path(exists=True))
@click.option("--name", "-n", default="default", help="知识库名称")
@click.option("--chunk-size", type=int, default=1000, help="文本块大小")
@click.option("--chunk-overlap", type=int, default=200, help="文本块重叠")
@click.option("--embedding-model", default="all-MiniLM-L6-v2", help="Embedding 模型")
def create_rag(
    docs_path: str,
    name: str,
    chunk_size: int,
    chunk_overlap: int,
    embedding_model: str,
):
    """创建向量检索知识库"""
    config = get_config()

    docs_path = Path(docs_path)
    rag_db_dir = config.rag_dir / name / "vector"

    console.print(f"📚 创建向量知识库: [cyan]{name}[/cyan]")
    console.print(f"📁 文档路径: {docs_path}")
    console.print(f"🔢 Chunk大小: {chunk_size}, 重叠: {chunk_overlap}")
    console.print(f"🤖 Embedding模型: {embedding_model}\n")

    try:
        # 加载文档
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("加载文档...", total=None)

            loader = DocumentLoader()
            documents = loader.load_directory(docs_path)

            if not documents:
                console.print("[yellow]未找到文档文件[/yellow]")
                return

            progress.update(task, description=f"已加载 {len(documents)} 个文档")

            # 分块
            task2 = progress.add_task("分割文档...", total=None)
            chunked_docs = loader.chunk_documents(
                documents,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            progress.update(task2, description=f"已分割为 {len(chunked_docs)} 个块")

        # 创建向量存储
        console.print("\n[bold]创建向量索引...[/bold]")
        console.print("[dim]这可能需要几分钟...[/dim]\n")

        vector_store = VectorStore(
            persist_directory=rag_db_dir,
            collection_name=name,
            embedding_model=embedding_model,
        )

        # 添加文档
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("向量化文档...", total=len(chunked_docs))

            batch_size = 100
            for i in range(0, len(chunked_docs), batch_size):
                batch = chunked_docs[i:i+batch_size]

                vector_store.add_documents(
                    documents=[doc["content"] for doc in batch],
                    metadatas=[doc["metadata"] for doc in batch],
                )

                progress.update(task, advance=len(batch))

        # 保存元数据
        metadata = {
            "name": name,
            "docs_path": str(docs_path),
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "embedding_model": embedding_model,
            "num_documents": len(documents),
            "num_chunks": len(chunked_docs),
            "type": "vector",
        }

        metadata_file = config.rag_dir / name / "metadata.json"
        metadata_file.parent.mkdir(parents=True, exist_ok=True)

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        console.print(f"\n✅ 知识库 [cyan]{name}[/cyan] 创建完成!")
        console.print(f"   📄 文档数: [cyan]{len(documents)}[/cyan]")
        console.print(f"   📦 文本块数: [cyan]{len(chunked_docs)}[/cyan]")
        console.print(f"\n使用以下命令查询:")
        console.print(f"   [cyan]ai-toolkit rag2 query {name} \"你的问题\"[/cyan]")

    except Exception as e:
        console.print(f"\n[red]创建失败: {e}[/red]")


@rag2_cli.command(name="query")
@click.argument("name")
@click.argument("question")
@click.option("--top-k", type=int, default=3, help="返回前K个相关片段")
@click.option("--show-context", is_flag=True, help="显示完整上下文")
def query_rag(name: str, question: str, top_k: int, show_context: bool):
    """查询向量知识库"""
    config = get_config()

    rag_db_dir = config.rag_dir / name / "vector"

    try:
        # 加载向量存储
        vector_store = VectorStore(
            persist_directory=rag_db_dir,
            collection_name=name,
        )

        console.print(f"🔍 查询知识库: [cyan]{name}[/cyan]")
        console.print(f"❓ 问题: {question}\n")

        # 查询
        results = vector_store.query(question, n_results=top_k)

        if not results["documents"][0]:
            console.print("[yellow]未找到相关内容[/yellow]")
            return

        # 显示结果
        for i, (doc, metadata, distance) in enumerate(
            zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ),
            1,
        ):
            similarity = (1 - distance) * 100

            console.print(
                Panel(
                    f"[cyan]文件:[/cyan] {metadata.get('filename', 'unknown')}\n"
                    f"[cyan]相似度:[/cyan] {similarity:.1f}%\n\n"
                    f"{doc[:500]}{'...' if len(doc) > 500 else ''}",
                    title=f"结果 {i}",
                    border_style="cyan",
                )
            )
            console.print()

    except Exception as e:
        console.print(f"[red]查询失败: {e}[/red]")
        console.print("[dim]提示: 确保知识库已创建[/dim]")


@rag2_cli.command(name="info")
@click.argument("name")
def rag_info(name: str):
    """显示知识库信息"""
    config = get_config()

    metadata_file = config.rag_dir / name / "metadata.json"

    if not metadata_file.exists():
        console.print(f"[red]知识库不存在: {name}[/red]")
        return

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    console.print(Panel(
        f"""[cyan]名称:[/cyan] {metadata['name']}
[cyan]类型:[/cyan] 向量检索 (ChromaDB)
[cyan]文档路径:[/cyan] {metadata['docs_path']}
[cyan]文档数量:[/cyan] {metadata.get('num_documents', 'N/A')}
[cyan]文本块数:[/cyan] {metadata.get('num_chunks', 'N/A')}
[cyan]Chunk大小:[/cyan] {metadata.get('chunk_size', 'N/A')}
[cyan]重叠:[/cyan] {metadata.get('chunk_overlap', 'N/A')}
[cyan]Embedding模型:[/cyan] {metadata.get('embedding_model', 'N/A')}""",
        title=f"📚 {name}",
        border_style="cyan",
    ))


@rag2_cli.command(name="list")
def list_rags():
    """列出所有向量知识库"""
    config = get_config()

    if not config.rag_dir.exists():
        console.print("[yellow]暂无知识库[/yellow]")
        return

    rag_dbs = []
    for kb_dir in config.rag_dir.iterdir():
        if kb_dir.is_dir():
            metadata_file = kb_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    if metadata.get("type") == "vector":
                        rag_dbs.append(metadata)

    if not rag_dbs:
        console.print("[yellow]暂无向量知识库[/yellow]")
        console.print("使用 [cyan]ai-toolkit rag2 create <path>[/cyan] 创建")
        return

    table = Table(title="📚 向量知识库", show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("类型", style="green")
    table.add_column("文档数", style="yellow")
    table.add_column("文本块数", style="blue")

    for kb in rag_dbs:
        table.add_row(
            kb["name"],
            "ChromaDB",
            str(kb.get("num_documents", "N/A")),
            str(kb.get("num_chunks", "N/A")),
        )

    console.print(table)
