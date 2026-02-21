"""
测试配置
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


@pytest.fixture
def sample_config():
    """示例配置"""
    return {
        "ollama_base_url": "http://localhost:11434",
        "ollama_timeout": 30,
        "rag_chunk_size": 1000,
        "rag_chunk_overlap": 200,
    }
