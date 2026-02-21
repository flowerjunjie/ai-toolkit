"""
配置验证
"""

from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel, Field, validator


class OllamaConfig(BaseModel):
    """Ollama 配置"""

    base_url: str = Field(default="http://localhost:11434")
    timeout: int = Field(default=30, ge=1, le=300)

    @validator("base_url")
    def validate_base_url(cls, v):
        """验证 URL 格式"""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Ollama URL 必须以 http:// 或 https:// 开头")
        return v

    async def check_connection(self) -> bool:
        """检查连接"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url)
                return response.status_code == 200
        except Exception:
            return False


class RAGConfig(BaseModel):
    """RAG 配置"""

    chunk_size: int = Field(default=1000, ge=100, le=10000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    top_k: int = Field(default=3, ge=1, le=20)

    @validator("chunk_overlap")
    def validate_overlap(cls, v, values):
        """验证重叠大小"""
        if "chunk_size" in values and v >= values["chunk_size"]:
            raise ValueError("chunk_overlap 必须小于 chunk_size")
        return v


class ToolkitConfig(BaseModel):
    """工具包配置"""

    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    rag: RAGConfig = Field(default_factory=RAGConfig)

    data_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "data")
    models_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "models")
    prompts_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "prompts")
    rag_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "rag")

    @validator("data_dir", "models_dir", "prompts_dir", "rag_dir")
    def validate_directories(cls, v):
        """验证目录路径"""
        if not isinstance(v, Path):
            v = Path(v)
        # 确保目录存在
        v.mkdir(parents=True, exist_ok=True)
        return v

    def validate(self) -> list[str]:
        """
        验证配置

        Returns:
            错误信息列表
        """
        errors = []

        # 验证 Ollama 连接
        import asyncio

        try:
            if not asyncio.run(self.ollama.check_connection()):
                errors.append(f"无法连接到 Ollama: {self.ollama.base_url}")
        except Exception as e:
            errors.append(f"Ollama 连接检查失败: {e}")

        return errors

    def is_valid(self) -> bool:
        """检查配置是否有效"""
        return len(self.validate()) == 0
