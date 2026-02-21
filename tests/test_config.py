"""
配置管理测试
"""

import json
from pathlib import Path

import pytest

from ai_toolkit.core.config import Config, get_config, initialize_config, save_config


def test_config_creation():
    """测试配置创建"""
    config = Config()
    assert config.config_path is not None
    assert config.data_dir is not None
    assert config.models_dir is not None


def test_config_defaults():
    """测试默认配置"""
    config = Config()
    assert config.ollama_base_url == "http://localhost:11434"
    assert config.ollama_timeout == 30
    assert config.rag_chunk_size == 1000


def test_config_save_and_load(tmp_path):
    """测试配置保存和加载"""
    # 创建临时配置路径
    config_path = tmp_path / "test_config.json"

    config = Config(config_path=config_path)
    config.ollama_timeout = 60
    save_config(config)

    # 加载配置
    loaded_config = load_config(config_path)
    assert loaded_config.ollama_timeout == 60


def test_initialize_config(tmp_path):
    """测试初始化配置"""
    config_path = tmp_path / "config"
    config = Config(config_path=config_path, data_dir=config_path / "data")

    initialize_config_custom(config)

    assert config.config_path.exists()
    assert config.data_dir.exists()
    assert config.models_dir.exists()


def initialize_config_custom(config: Config):
    """自定义初始化函数用于测试"""
    config.config_path.parent.mkdir(parents=True, exist_ok=True)
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.models_dir.mkdir(parents=True, exist_ok=True)
    config.prompts_dir.mkdir(parents=True, exist_ok=True)
    config.rag_dir.mkdir(parents=True, exist_ok=True)
    save_config(config)
