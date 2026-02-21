"""
API Key 管理器测试
"""

import pytest
from ai_toolkit.core.api_manager import APIKey, APIKeyManager


class TestAPIKey:
    """APIKey 类测试"""

    def test_api_key_creation(self):
        """测试 API Key 创建"""
        key = APIKey(
            api_key="test-key",
            base_url="https://api.test.com",
            model="test-model",
            provider="test-provider",
        )

        assert key.api_key == "test-key"
        assert key.base_url == "https://api.test.com"
        assert key.model == "test-model"
        assert key.provider == "test-provider"

    def test_mark_used(self):
        """测试标记使用"""
        key = APIKey(
            api_key="test-key",
            base_url="https://api.test.com",
            model="test-model",
            provider="test-provider",
        )

        assert key.request_count == 0
        key.mark_used()
        assert key.request_count == 1
        key.mark_used()
        assert key.request_count == 2

    def test_mark_error(self):
        """测试标记错误"""
        key = APIKey(
            api_key="test-key",
            base_url="https://api.test.com",
            model="test-model",
            provider="test-provider",
        )

        assert key.is_available()
        key.mark_error()
        assert key.error_count == 1
        assert key.is_available()

        # 标记10次错误
        for _ in range(10):
            key.mark_error()

        assert not key.is_available()


class TestAPIKeyManager:
    """APIKeyManager 类测试"""

    def test_manager_creation(self):
        """测试管理器创建"""
        manager = APIKeyManager()
        assert manager is not None
        assert manager.api_keys is not None

    def test_get_next_key(self):
        """测试获取下一个 Key"""
        manager = APIKeyManager()

        # 添加测试 Key
        manager.api_keys = [
            APIKey("key1", "https://api1.com", "model1", "provider1"),
            APIKey("key2", "https://api2.com", "model2", "provider2"),
        ]
        manager.current_cycle = cycle(manager.api_keys)

        key1 = manager.get_next_key()
        key2 = manager.get_next_key()

        assert key1.api_key == "key1"
        assert key2.api_key == "key2"

    def test_reset_errors(self):
        """测试重置错误"""
        manager = APIKeyManager()

        key = APIKey("test-key", "https://api.test.com", "test-model", "test-provider")
        for _ in range(10):
            key.mark_error()

        assert not key.is_available()

        manager.api_keys = [key]
        manager.reset_errors()

        assert key.is_available()

    def test_get_status(self):
        """测试获取状态"""
        manager = APIKeyManager()

        manager.api_keys = [
            APIKey("key1", "https://api1.com", "model1", "provider1"),
        ]

        status = manager.get_status()

        assert len(status) == 1
        assert status[0]["provider"] == "provider1"
        assert status[0]["model"] == "model1"
        assert status[0]["available"] is True
