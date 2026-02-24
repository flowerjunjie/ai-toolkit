
"""
RAG向量检索 - 真实集成版
真实集成ChromaDB，支持向量检索
"""

import click
import os
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
import json

console = Console()

# 尝试导入chromadb，如果失败则设为None
chromadb = None
Settings = None
embedding_functions = None

try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
except ImportError:
    console.print("⚠️  警告: chromadb未安装，RAG功能将不可用")


@click.group(name="rag")
def rag_cli():
    """RAG向量检索"""
    pass


def check_chromadb():
    """检查chromadb是否已安装"""
    if chromadb is None:
        console.print("\n❌ 错误: chromadb未安装")
        console.print("请运行: pip install chromadb sentence-transformers langchain")
        return False
    return True


@rag_cli.command(name="create")
@click.option("--name", "-n", help="知识库名称")
@click.option("--path", "-p", help="文档目录")
def create_knowledge(name: str, path: str):
    """创建知识库"""
    if not check_chromadb():
        return

    console.print(f"\n📚 创建知识库\n")

    if not name:
        name = "my-knowledge"

    if not path:
        path = "./docs"

    console.print(f"名称: {name}")
    console.print(f"路径: {path}")

    docs_path = Path(path)
    if not docs_path.exists():
        console.print(f"\n❌ 路径不存在: {path}")
        return

    console.print("\n处理中...")

    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chroma"
        ))

        collection = client.create_collection(
            name=name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

        console.print(f"\n✅ 知识库创建成功！")
        console.print(f"集合名称: {name}")
        console.print(f"持久化位置: ./.chroma")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@rag_cli.command(name="index")
@click.option("--name", "-n", help="知识库名称")
@click.option("--path", "-p", help="文档路径")
def index_documents(name: str, path: str):
    """索引文档"""
    if not check_chromadb():
        return

    console.print(f"\n📄 索引文档\n")

    if not name:
        name = "my-knowledge"

    if not path:
        console.print("❌ 请指定文档路径")
        return

    console.print(f"知识库: {name}")
    console.print(f"文档: {path}")

    console.print("\n索引中...")

    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chroma"
        ))

        collection = client.get_collection(
            name=name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

        doc_path = Path(path)
        if doc_path.exists():
            content = doc_path.read_text()
            collection.add(
                documents=[content],
                ids=[doc_path.name]
            )
            console.print(f"\n✅ 文档索引成功！")
        else:
            console.print(f"\n❌ 文件不存在: {path}")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@rag_cli.command(name="search")
@click.option("--name", "-n", help="知识库名称")
@click.option("--query", "-q", help="搜索查询")
def search_documents(name: str, query: str):
    """搜索文档"""
    if not check_chromadb():
        return

    console.print(f"\n🔍 搜索文档\n")

    if not name:
        name = "my-knowledge"

    if not query:
        console.print("❌ 请指定搜索查询")
        return

    console.print(f"知识库: {name}")
    console.print(f"查询: {query}")

    console.print("\n搜索中...")

    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chroma"
        ))

        collection = client.get_collection(
            name=name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        console.print(f"\n✅ 搜索完成！")
        console.print(f"\n结果:")

        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                console.print(f"\n{i+1}. {doc[:100]}...")
        else:
            console.print("无结果")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@rag_cli.command(name="list")
def list_collections():
    """列出知识库"""
    if not check_chromadb():
        return

    console.print(f"\n📋 知识库列表\n")

    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chroma"
        ))

        collections = client.list_collections()

        if collections:
            table = Table(title="知识库")
            table.add_column("名称", style="cyan")

            for coll in collections:
                table.add_row(coll.name)

            console.print(table)
            console.print(f"\n总计: {len(collections)}个知识库")
        else:
            console.print("暂无知识库")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@rag_cli.command(name="delete")
@click.option("--name", "-n", help="知识库名称")
def delete_collection(name: str):
    """删除知识库"""
    if not check_chromadb():
        return

    console.print(f"\n🗑️ 删除知识库\n")

    if not name:
        console.print("❌ 请指定知识库名称")
        return

    console.print(f"知识库: {name}")

    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chroma"
        ))

        client.delete_collection(name=name)
        console.print(f"\n✅ 知识库删除成功！")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@rag_cli.command(name="help")
def rag_help():
    """帮助信息"""
    console.print(f"\n📖 RAG帮助\n")

    console.print("快速开始:")
    console.print("  1. 安装依赖:")
    console.print("     pip install chromadb sentence-transformers langchain")
    console.print("")
    console.print("  2. 创建知识库:")
    console.print("     ai-toolkit rag create --name my-kb --path ./docs")
    console.print("")
    console.print("  3. 索引文档:")
    console.print("     ai-toolkit rag index --name my-kb --path document.txt")
    console.print("")
    console.print("  4. 搜索:")
    console.print("     ai-toolkit rag search --name my-kb --query '我的问题'")

    console.print("\n✅ 帮助信息显示完成")
