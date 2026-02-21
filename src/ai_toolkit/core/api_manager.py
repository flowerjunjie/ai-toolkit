"""
API Key 管理器 - 轮换使用多个 API Key
"""

from typing import List, Dict, Any, Optional
from itertools import cycle
import time
import requests


class APIKey:
    """API Key 配置"""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        provider: str,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.provider = provider
        self.request_count = 0
        self.last_used = 0
        self.error_count = 0

    def is_available(self) -> bool:
        """检查 API Key 是否可用"""
        # 简单的策略：错误次数 < 10
        return self.error_count < 10

    def mark_used(self):
        """标记已使用"""
        self.request_count += 1
        self.last_used = time.time()

    def mark_error(self):
        """标记错误"""
        self.error_count += 1


class APIKeyManager:
    """API Key 管理器 - 轮换使用"""

    def __init__(self):
        """初始化 API Key 管理器"""
        self.api_keys: List[APIKey] = []
        self.current_cycle = None
        self.initialize_keys()

    def initialize_keys(self):
        """初始化所有 API Key"""
        keys_config = [
            # BigModel - glm-4.7
            {
                "api_key": "9e4dc7223ebe45b0a93f486d5e4fb524.9w24QSuSJkS2bS3D",
                "base_url": "https://open.bigmodel.cn/api/anthropic",
                "model": "glm-4.7",
                "provider": "bigmodel",
            },
            {
                "api_key": "e14f3609b81c42649ef4555af4c8144d.aGfi49Q5ZyNZKilf",
                "base_url": "https://open.bigmodel.cn/api/anthropic",
                "model": "glm-4.7",
                "provider": "bigmodel",
            },
            {
                "api_key": "3912dd98a72a4a84a60655ee46814a2a.W9cr2ViWxqw5XPri",
                "base_url": "https://open.bigmodel.cn/api/anthropic",
                "model": "glm-4.7",
                "provider": "bigmodel",
            },
            # BigModel - glm-5 (Pro)
            {
                "api_key": "5b2c1fa2ab524de2ab1ad87e39dea7e8.BmT1eCr9TArqA0ju",
                "base_url": "https://open.bigmodel.cn/api/anthropic",
                "model": "glm-5",
                "provider": "bigmodel-pro",
            },
            {
                "api_key": "f7099b3140a244329dcfd263b3ce5da6.xNkPaGPRmEbpqutl",
                "base_url": "https://open.bigmodel.cn/api/anthropic",
                "model": "glm-5",
                "provider": "bigmodel-pro",
            },
            # MiniMax
            {
                "api_key": "sk-cp-COh56PJjRSyf-vFNtvd3nhgR88ve6C5ayKL8SwSUReDAY6VHVFd6kPmIN5HI3-pY2OIgbsua9nu5FEpGb1uHBo3yzD2Lv-ZRf3zzqKBLouDl8C2rubSzV30",
                "base_url": "https://api.minimaxi.com/anthropic",
                "model": "MiniMax-M2.5",
                "provider": "minimax",
            },
            {
                "api_key": "sk-cp-xzSKFnHO45-GQ9YUfP8rvpJk2uRtQMweOhf1DbPsojpYciT0SevcjhKO2sR0PtQ_f3kyeXOXO-rk4qqtMWt3TlVzOuKz-SZqzbuexkgyoXLHDl6zvpdxZRw",
                "base_url": "https://api.minimaxi.com/anthropic",
                "model": "MiniMax-M2.5",
                "provider": "minimax",
            },
            # Kimi
            {
                "api_key": "sk-kimi-PUQvLapp4UDvD2en5dLLYwRKayxQoe132tB6cJYOWgeLrDJH7oz81KnfGt2drFBZ",
                "base_url": "https://api.kimi.com/coding/",
                "model": "kimi-for-coding",
                "provider": "kimi",
            },
            {
                "api_key": "sk-kimi-TNRtsCiji5dpKG6jfTxbgNSpJrfdasOPDx9gLOUn18WPwNRfryZCmOxdsRLyUjqx",
                "base_url": "https://api.kimi.com/coding/",
                "model": "kimi-for-coding",
                "provider": "kimi",
            },
            # Doubao
            {
                "api_key": "59fdb627-fad1-41f7-b409-c904c57d1423",
                "base_url": "https://ark.cn-beijing.volces.com/api/coding",
                "model": "Doubao-Seed-2.0-Code",
                "provider": "doubao",
            },
        ]

        # 创建 APIKey 对象
        self.api_keys = [APIKey(**config) for config in keys_config]

        # 创建轮换周期
        self.current_cycle = cycle(self.api_keys)

    def get_next_key(self, provider: Optional[str] = None) -> APIKey:
        """
        获取下一个可用的 API Key

        Args:
            provider: 指定提供商（可选）

        Returns:
            APIKey 对象
        """
        if provider:
            # 过滤指定提供商
            provider_keys = [k for k in self.api_keys if k.provider == provider and k.is_available()]
            if not provider_keys:
                # 如果没有可用的，使用所有可用的
                return self.get_next_key(None)
            return cycle(provider_keys).__next__()

        # 轮换获取
        max_attempts = len(self.api_keys) * 2  # 防止无限循环
        for _ in range(max_attempts):
            api_key = next(self.current_cycle)
            if api_key.is_available():
                api_key.mark_used()
                return api_key

        # 如果所有都不可用，重置错误计数并重试
        self.reset_errors()
        return self.get_next_key(provider)

    def mark_key_error(self, api_key: APIKey):
        """
        标记 API Key 错误

        Args:
            api_key: 出错的 API Key
        """
        api_key.mark_error()

    def reset_errors(self):
        """重置所有 API Key 的错误计数"""
        for key in self.api_keys:
            key.error_count = 0

    def get_status(self) -> List[Dict[str, Any]]:
        """
        获取所有 API Key 的状态

        Returns:
            状态列表
        """
        return [
            {
                "provider": key.provider,
                "model": key.model,
                "available": key.is_available(),
                "request_count": key.request_count,
                "error_count": key.error_count,
                "last_used": key.last_used,
            }
            for key in self.api_keys
        ]

    def get_available_count(self) -> int:
        """获取可用 API Key 数量"""
        return sum(1 for key in self.api_keys if key.is_available())

    def get_total_count(self) -> int:
        """获取总 API Key 数量"""
        return len(self.api_keys)


# 全局单例
_api_key_manager: Optional[APIKeyManager] = None


def get_api_manager() -> APIKeyManager:
    """获取 API Key 管理器单例"""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager
