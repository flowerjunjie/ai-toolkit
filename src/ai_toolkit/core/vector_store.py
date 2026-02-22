"""
向量存储 - 基于 ChromaDB 的向量检索
"""

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:
    """向量存储管理器"""

    def __init__(
        self,
        persist_directory: Union[str, Path],
        collection_name: str = "documents",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        """
        初始化向量存储

        Args:
            persist_directory: 持久化目录
            collection_name: 集合名称
            embedding_model: Embedding 模型名称
        """
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
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        添加文档到向量存储

        Args:
            documents: 文档列表
            metadatas: 元数据列表
            ids: 文档 ID 列表

        Returns:
            文档 ID 列表
        """
        # 生成 embeddings
        embeddings = self.embedder.encode(documents).tolist()

        # 生成 ID（如果未提供）
        if ids is None:
            ids = [self._generate_id(doc) for doc in documents]

        # 添加到集合
        self.collection.add(
            embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids
        )

        return ids

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        查询相似文档

        Args:
            query_text: 查询文本
            n_results: 返回结果数量
            where: 过滤条件

        Returns:
            查询结果
        """
        # 生成查询向量
        query_embedding = self.embedder.encode([query_text]).tolist()

        # 查询
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where,
        )

        return results

    def delete(self, ids: Optional[List[str]] = None) -> None:
        """
        删除文档

        Args:
            ids: 要删除的文档 ID 列表
        """
        if ids:
            self.collection.delete(ids=ids)

    def update(
        self,
        ids: List[str],
        documents: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        更新文档

        Args:
            ids: 文档 ID 列表
            documents: 新文档内容
            metadatas: 新元数据
        """
        embeddings = None
        if documents:
            embeddings = self.embedder.encode(documents).tolist()

        self.collection.update(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息

        Returns:
            集合信息
        """
        count = self.collection.count()

        return {
            "name": self.collection.name,
            "count": count,
            "persist_directory": str(self.persist_directory),
        }

    def clear(self) -> None:
        """清空集合"""
        # 删除并重建集合
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name, metadata={"hnsw:space": "cosine"}
        )

    @staticmethod
    def _generate_id(text: str) -> str:
        """
        生成文档 ID

        Args:
            text: 文本内容

        Returns:
            文档 ID
        """
        return hashlib.md5(text.encode()).hexdigest()[:16]
