"""
工具函数测试
"""

import pytest

from ai_toolkit.utils import format_duration, format_size, sanitize_filename, validate_model_name


def test_format_size():
    """测试大小格式化"""
    assert format_size(500) == "500.00 B"
    assert format_size(1024) == "1.00 KB"
    assert format_size(1024 * 1024) == "1.00 MB"
    assert format_size(1024 * 1024 * 1024) == "1.00 GB"


def test_format_duration():
    """测试时长格式化"""
    assert format_duration(0.5) == "500ms"
    assert format_duration(5) == "5.0s"
    assert format_duration(65) == "1m 5s"
    assert format_duration(3665) == "61m 5s"


def test_validate_model_name():
    """测试模型名称验证"""
    assert validate_model_name("llama3.2") == True
    assert validate_model_name("mistral-7b") == True
    assert validate_model_name("gpt_4") == True
    assert validate_model_name("") == False
    assert validate_model_name("invalid@name") == False


def test_sanitize_filename():
    """测试文件名清理"""
    assert sanitize_filename("test_file.txt") == "test_file.txt"
    assert sanitize_filename("file<>name") == "file__name"
    assert sanitize_filename("file|name?") == "file_name_"
    assert sanitize_filename("  file  ") == "file"
