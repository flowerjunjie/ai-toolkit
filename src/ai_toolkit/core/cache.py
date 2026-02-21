"""
缓存工具 - 提升性能
"""

import functools
import hashlib
import pickle
import time
from pathlib import Path
from typing import Any, Callable, Optional


def lru_cache_with_ttl(maxsize: int = 128, ttl: int = 3600):
    """
    带TTL的LRU缓存

    Args:
        maxsize: 最大缓存大小
        ttl: 生存时间（秒）

    Returns:
        装饰器
    """
    cache = {}
    timestamps = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()

            # 检查缓存
            if key in cache:
                # 检查是否过期
                if time.time() - timestamps[key] < ttl:
                    return cache[key]
                else:
                    # 过期，删除
                    del cache[key]
                    del timestamps[key]

            # 执行函数
            result = func(*args, **kwargs)

            # 存入缓存
            cache[key] = result
            timestamps[key] = time.time()

            # 限制缓存大小
            if len(cache) > maxsize:
                # 删除最旧的
                oldest_key = min(timestamps, key=timestamps.get)
                del cache[oldest_key]
                del timestamps[oldest_key]

            return result

        return wrapper

    return decorator


class DiskCache:
    """磁盘缓存"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        初始化磁盘缓存

        Args:
            cache_dir: 缓存目录
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".ai-toolkit" / "cache"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            缓存值，不存在返回 None
        """
        cache_file = self.cache_dir / f"{key}.cache"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "rb") as f:
                data = pickle.load(f)

            # 检查是否过期
            if time.time() > data.get("expires", 0):
                cache_file.unlink()
                return None

            return data.get("value")
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 生存时间（秒）
        """
        cache_file = self.cache_dir / f"{key}.cache"

        data = {
            "value": value,
            "expires": time.time() + ttl,
        }

        with open(cache_file, "wb") as f:
            pickle.dump(data, f)

    def clear(self):
        """清空缓存"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

    def cleanup(self):
        """清理过期缓存"""
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, "rb") as f:
                    data = pickle.load(f)

                if time.time() > data.get("expires", 0):
                    cache_file.unlink()
            except Exception:
                cache_file.unlink()


# 全局缓存实例
_cache: Optional[DiskCache] = None


def get_cache() -> DiskCache:
    """获取全局缓存实例"""
    global _cache
    if _cache is None:
        _cache = DiskCache()
    return _cache


def cached_disk(ttl: int = 3600):
    """
    磁盘缓存装饰器

    Args:
        ttl: 生存时间（秒）

    Returns:
        装饰器
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = f"{func.__name__}_{hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()}"

            # 尝试从缓存获取
            cache = get_cache()
            result = cache.get(key)

            if result is not None:
                return result

            # 执行函数
            result = func(*args, **kwargs)

            # 存入缓存
            cache.set(key, result, ttl)

            return result

        return wrapper

    return decorator
