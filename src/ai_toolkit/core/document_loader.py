"""
文档加载器 - 支持多种文档格式
"""

from pathlib import Path
from typing import List, Dict, Any
import re


class DocumentLoader:
    """文档加载器"""

    def __init__(self):
        """初始化文档加载器"""
        self.supported_extensions = [".txt", ".md", ".rst", ".py", ".js", ".html", ".css"]

    def load_directory(
        self,
        directory: Path | str,
        extensions: Optional[List[str]] = None,
        max_size: int = 10 * 1024 * 1024,  # 10MB
    ) -> List[Dict[str, Any]]:
        """
        加载目录中的所有文档

        Args:
            directory: 目录路径
            extensions: 文件扩展名列表
            max_size: 最大文件大小

        Returns:
            文档列表
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        if extensions is None:
            extensions = self.supported_extensions

        documents = []

        # 遍历目录
        for ext in extensions:
            for file_path in directory.rglob(f"*{ext}"):
                try:
                    # 检查文件大小
                    if file_path.stat().st_size > max_size:
                        continue

                    # 加载文档
                    doc = self.load_file(file_path)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    # 跳过无法加载的文件
                    continue

        return documents

    def load_file(self, file_path: Path | str) -> Optional[Dict[str, Any]]:
        """
        加载单个文件

        Args:
            file_path: 文件路径

        Returns:
            文档字典
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return None

        # 读取文件内容
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if not content.strip():
                return None

            return {
                "content": content,
                "metadata": {
                    "source": str(file_path),
                    "filename": file_path.name,
                    "extension": file_path.suffix,
                    "size": file_path.stat().st_size,
                }
            }
        except Exception:
            return None

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> List[str]:
        """
        将文本分割成块

        Args:
            text: 输入文本
            chunk_size: 块大小
            chunk_overlap: 重叠大小

        Returns:
            文本块列表
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size

            # 尝试在句子边界分割
            if end < text_length:
                # 寻找最近的句子结束符
                for sep in [".", "\n", "!", "?"]:
                    sep_pos = text.rfind(sep, start, end)
                    if sep_pos != -1:
                        end = sep_pos + 1
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # 移动到下一个块（带重叠）
            start = end - chunk_overlap

            if start >= text_length:
                break

        return chunks

    def chunk_documents(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> List[Dict[str, Any]]:
        """
        将文档列表分割成块

        Args:
            documents: 文档列表
            chunk_size: 块大小
            chunk_overlap: 重叠大小

        Returns:
            分块后的文档列表
        """
        chunked_docs = []

        for doc in documents:
            content = doc["content"]
            metadata = doc.get("metadata", {})

            # 分割文本
            chunks = self.chunk_text(content, chunk_size, chunk_overlap)

            # 为每个块创建文档
            for i, chunk in enumerate(chunks):
                chunked_docs.append({
                    "content": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_id": i,
                        "total_chunks": len(chunks),
                    }
                })

        return chunked_docs
