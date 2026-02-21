"""
API Key 管理器 - 从环境变量或配置文件加载
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from itertools import cycle


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
        return self.error_count < 10

    def mark_used(self):
        """标记已使用"""
        self.request_count += 1
        self.last_used = time.time()

    def mark_error(self):
        """标记错误"""
        self.error_count += 1


class APIKeyManager:
    """API Key 管理器 - 从环境变量或配置文件加载"""

    def __init__(self):
        """初始化 API Key 管理器"""
        self.api_keys: List[APIKey] = []
        self.current_cycle = None
        self.initialize_keys()

    def initialize_keys(self):
        """从环境变量或配置文件加载 API Key"""
        # 方法1: 从环境变量加载
        env_keys = self._load_from_env()
        if env_keys:
            self.api_keys = env_keys
            self.current_cycle = cycle(self.api_keys)
            return

        # 方法2: 从配置文件加载
        config_keys = self._load_from_config()
        if config_keys:
            self.api_keys = config_keys
            self.current_cycle = cycle(self.api_keys)
            return

        # 方法3: 空列表（不包含任何硬编码）
        self.api_keys = []
        self.current_cycle = cycle(self.api_keys)

    def _load_from_env(self) -> List[APIKey]:
        """从环境变量加载 API Key"""
        keys = []

        # BigModel
        for i in range(1, 11):  # BIGMODEL_1 到 BIGMODEL_10
            key = os.getenv(f"BIGMODEL_{i}")
            if key:
                keys.append(APIKey(
                    api_key=key,
                    base_url="https://open.bigmodel.cn/api/anthropic",
                    model="glm-4.7" if i <= 3 else "glm-5",
                    provider="bigmodel",
                ))

        # MiniMax
        for i in range(1, 11):  # MINIMAX_1 到 MINIMAX_10
            key = os.getenv(f"MINIMAX_{i}")
            if key:
                keys.append(APIKey(
                    api_key=key,
                    base_url="https://api.minimaxi.com/anthropic",
                    model="MiniMax-M2.5",
                    provider="minimax",
                ))

        # Kimi
        for i in range(1, 11):  # KIMI_1 到 KIMI_10
            key = os.getenv(f"KIMI_{i}")
            if key:
                keys.append(APIKey(
                    api_key=key,
                    base_url="https://api.kimi.com/coding/",
                    model="kimi-for-coding",
                    provider="kimi",
                ))

        # Doubao
        for i in range(1, 11):  # DOUBAO_1 到 DOUBAO_10
            key = os.getenv(f"DOUBAO_{i}")
            if key:
                keys.append(APIKey(
                    api_key=key,
                    base_url="https://ark.cn-beijing.volces.com/api/coding",
                    model="Doubao-Seed-2.0-Code",
                    provider="doubao",
                ))

        return keys

    def _load_from_config(self) -> List[APIKey]:
        """从配置文件加载 API Key"""
        config_file = Path.home() / ".ai-toolkit" / "api_keys.json"

        if not config_file.exists():
            return []

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            keys = []
            for key_config in config.get("api_keys", []):
                keys.append(APIKey(
                    api_key=key_config["api_key"],
                    base_url=key_config["base_url"],
                    model=key_config["model"],
                    provider=key_config["provider"],
                ))

            return keys
        except Exception:
            return []

    def get_next_key(self, provider: Optional[str] = None) -> APIKey:
        """
        获取下一个可用的 API Key

        Args:
            provider: 指定提供商（可选）

        Returns:
            APIKey 对象
        """
        if provider:
            provider_keys = [k for k in self.api_keys if k.provider == provider and k.is_available()]
            if provider_keys:
                return cycle(provider_keys).__next__()

        # 轮换获取
        max_attempts = len(self.api_keys) * 2
        for _ in range(max_attempts):
            api_key = next(self.current_cycle)
            if api_key.is_available():
                api_key.mark_used()
                return api_key

        # 如果所有都不可用，重置错误计数并重试
        self.reset_errors()
        return self.get_next_key(provider)

    def mark_key_error(self, api_key: APIKey):
        """标记 API Key 错误"""
        api_key.mark_error()

    def reset_errors(self):
        """重置所有 API Key 的错误计数"""
        for key in self.api_keys:
            key.error_count = 0

    def get_status(self) -> List[Dict[str, Any]]:
        """获取所有 API Key 的状态"""
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
