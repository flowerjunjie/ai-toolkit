
"""
向量存储 - 基于 ChromaDB 的向量检索
"""

import hashlib
from pathlib import Path
import warnings

# 尝试导入可选依赖
chromadb = None
SentenceTransformer = None

try:
    import chromadb
except ImportError:
    warnings.warn("chromadb未安装，VectorStore功能将不可用", ImportWarning)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    warnings.warn("sentence-transformers未安装，VectorStore功能将不可用", ImportWarning)


class VectorStore:
    """向量存储管理器"""

    def __init__(
        self,
        persist_directory,
        collection_name = "documents",
        embedding_model = "all-MiniLM-L6-v2",
    ):
        """
        初始化向量存储

        Args:
            persist_directory: 持久化目录
            collection_name: 集合名称
            embedding_model: Embedding 模型名称
        """
        # 检查依赖是否已安装
        if chromadb is None:
            raise ImportError("chromadb未安装，请运行: pip install chromadb")
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers未安装，请运行: pip install sentence-transformers")

        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # 初始化 ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))

        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

        # 初始化 Embedding 模型
        self.embedder = SentenceTransformer(embedding_model)

    def add_documents(
        self,
        documents,
        metadatas = None,
        ids = None,
    ):
        """
        添加文档到向量存储

        Args:
            documents: 文档内容列表
            metadatas: 元数据列表（可选）
            ids: 文档ID列表（可选，自动生成如果未提供）

        Returns:
            文档ID列表
        """
        # 生成ID（如果未提供）
        if ids is None:
            ids = [
                hashlib.md5(doc.encode()).hexdigest() 
                for doc in documents
            ]

        # 生成embeddings
        embeddings = self.embedder.encode(documents).tolist()

        # 添加到集合
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        return ids

    def search(
        self,
        query,
        n_results = 5,
    ):
        """
        搜索相似文档

        Args:
            query: 查询文本
            n_results: 返回结果数量

        Returns:
            搜索结果
        """
        # 生成查询embedding
        query_embedding = self.embedder.encode([query]).tolist()

        # 搜索
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results

    def delete(self, ids):
        """
        删除文档

        Args:
            ids: 文档ID列表
        """
        self.collection.delete(ids=ids)

    def get_all(self):
        """
        获取所有文档

        Returns:
            所有文档
        """
        return self.collection.get()

    def count(self):
        """
        获取文档数量

        Returns:
            文档数量
        """
        return self.collection.count()

    def clear(self):
        """清空集合"""
        all_ids = self.collection.get()["ids"]
        if all_ids:
            self.collection.delete(ids=all_ids)
