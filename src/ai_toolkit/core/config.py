"""
配置管理
"""

import json
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, Field
from functools import lru_cache
import threading

# 配置锁，防止并发写入
_config_lock = threading.Lock()
# 配置缓存
_config_cache: Optional["Config"] = None


class Config(BaseModel):
    """配置模型"""

    config_path: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "config.json")
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "data")
    models_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "models")
    prompts_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "prompts")
    rag_dir: Path = Field(default_factory=lambda: Path.home() / ".ai-toolkit" / "rag")

    # Ollama配置
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout: int = 30

    # RAG配置
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 200
    rag_top_k: int = 3

    class Config:
        arbitrary_types_allowed = True


@lru_cache(maxsize=1)
def get_config() -> Config:
    """获取配置实例（带缓存）"""
    global _config
    if _config is None:
        _config = Config()
        _config = load_config()
    return _config


def load_config(path: Optional[Path] = None) -> Config:
    """从文件加载配置"""
    if path:
        config_path = path
    else:
        config_path = Path.home() / ".ai-toolkit" / "config.json"

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Config(**data)
    else:
        return Config()


def save_config(config: Config) -> None:
    """保存配置到文件"""
    config_path = config.config_path
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=2, ensure_ascii=False)


def initialize_config() -> Config:
    """初始化配置"""
    config = Config()

    # 创建必要的目录
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.models_dir.mkdir(parents=True, exist_ok=True)
    config.prompts_dir.mkdir(parents=True, exist_ok=True)
    config.rag_dir.mkdir(parents=True, exist_ok=True)

    # 保存配置
    save_config(config)

    return config
