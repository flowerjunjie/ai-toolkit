"""
HTTP客户端优化 - 连接池和复用
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
import time


class OptimizedHTTPClient:
    """优化的HTTP客户端"""

    def __init__(
        self,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        """
        初始化优化的HTTP客户端

        Args:
            pool_connections: 连接池大小
            pool_maxsize: 最大连接数
            max_retries: 最大重试次数
            backoff_factor: 退避因子
        """
        self.session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        # 配置适配器
        adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=retry_strategy,
        )

        # 挂载适配器
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url: str, **kwargs) -> requests.Response:
        """GET请求"""
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """POST请求"""
        return self.session.post(url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.session.put(url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.session.delete(url, **kwargs)

    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局客户端实例
_http_client: Optional[OptimizedHTTPClient] = None


def get_http_client() -> OptimizedHTTPClient:
    """获取全局HTTP客户端"""
    global _http_client
    if _http_client is None:
        _http_client = OptimizedHTTPClient()
    return _http_client
