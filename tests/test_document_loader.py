"""
工具函数测试
"""

import pytest
from ai_toolkit.utils.helpers import (
    format_size,
    format_duration,
    validate_model_name,
    sanitize_filename,
)


class TestFormatSize:
    """格式化大小测试"""

    def test_format_size_bytes(self):
        """测试字节格式化"""
        assert format_size(500) == "500.00 B"
        assert format_size(1024) == "1.00 KB"

    def test_format_size_kb(self):
        """测试KB格式化"""
        assert format_size(1024 * 5) == "5.00 KB"
        assert format_size(1024 * 1024) == "1.00 MB"

    def test_format_size_gb(self):
        """测试GB格式化"""
        assert format_size(1024 * 1024 * 1024) == "1.00 GB"


class TestFormatDuration:
    """格式化时长测试"""

    def test_format_duration_ms(self):
        """测试毫秒格式化"""
        assert format_duration(0.5) == "500ms"

    def test_format_duration_seconds(self):
        """测试秒格式化"""
        assert format_duration(5) == "5.0s"
        assert format_duration(45) == "45.0s"

    def test_format_duration_minutes(self):
        """测试分钟格式化"""
        assert format_duration(65) == "1m 5s"
        assert format_duration(3665) == "61m 5s"


class TestValidateModelName:
    """模型名称验证测试"""

    def test_valid_names(self):
        """测试有效名称"""
        assert validate_model_name("llama3.2") is True
        assert validate_model_name("mistral-7b") is True
        assert validate_model_name("gpt_4") is True

    def test_invalid_names(self):
        """测试无效名称"""
        assert validate_model_name("") is False
        assert validate_model_name("invalid@name") is False


class TestSanitizeFilename:
    """文件名清理测试"""

    def test_sanitize_basic(self):
        """测试基本清理"""
        assert sanitize_filename("test_file.txt") == "test_file.txt"

    def test_sanitize_special_chars(self):
        """测试特殊字符清理"""
        result = sanitize_filename("file<>name")
        assert "<" not in result
        assert ">" not in result

    def test_sanitize_spaces(self):
        """测试空格清理"""
        result = sanitize_filename("  file  ")
        assert result.strip() == result
