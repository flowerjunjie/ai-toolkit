"""
向量存储测试
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from ai_toolkit.core.vector_store import VectorStore


class TestVectorStore:
    """VectorStore 类测试"""

    @pytest.fixture
    def temp_dir(self):
        """临时目录"""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    def test_vector_store_creation(self, temp_dir):
        """测试向量存储创建"""
        store = VectorStore(
            persist_directory=temp_dir,
            collection_name="test",
        )

        assert store is not None
        assert store.persist_directory == temp_dir

    def test_add_documents(self, temp_dir):
        """测试添加文档"""
        store = VectorStore(
            persist_directory=temp_dir,
            collection_name="test",
        )

        documents = ["文档1", "文档2", "文档3"]
        ids = store.add_documents(documents)

        assert len(ids) == 3
        assert all(isinstance(id, str) for id in ids)

    def test_query_documents(self, temp_dir):
        """测试查询文档"""
        store = VectorStore(
            persist_directory=temp_dir,
            collection_name="test",
        )

        documents = ["Python是一种编程语言", "JavaScript是Web开发语言"]
        store.add_documents(documents)

        results = store.query("编程语言", n_results=1)

        assert results is not None
        assert "documents" in results

    def test_collection_info(self, temp_dir):
        """测试获取集合信息"""
        store = VectorStore(
            persist_directory=temp_dir,
            collection_name="test",
        )

        info = store.get_collection_info()

        assert info["name"] == "test"
        assert "count" in info
