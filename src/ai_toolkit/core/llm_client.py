"""
LLM 客户端 - 支持多个提供商
"""

from typing import Any, Dict, List, Optional

import requests

from ai_toolkit.core.api_manager import APIKey, get_api_manager


class LLMClient:
    """LLM 客户端 - 统一接口"""

    def __init__(self, provider: Optional[str] = None):
        """
        初始化 LLM 客户端

        Args:
            provider: 指定提供商（可选）
        """
        self.api_manager = get_api_manager()
        self.provider = provider
        self.current_key: Optional[APIKey] = None

    def get_api_key(self) -> APIKey:
        """获取 API Key"""
        self.current_key = self.api_manager.get_next_key(self.provider)
        return self.current_key

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            max_tokens: 最大 token 数
            temperature: 温度参数
            stream: 是否流式输出

        Returns:
            生成的文本
        """
        api_key = self.get_api_key()

        # 构建请求
        headers = {
            "x-api-key": api_key.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        data = {
            "model": api_key.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": stream,
        }

        try:
            response = requests.post(
                f"{api_key.base_url}/v1/messages",
                headers=headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()

            # 提取生成的文本
            if "content" in result and len(result["content"]) > 0:
                return result["content"][0].get("text", "")
            return ""

        except requests.exceptions.HTTPError as e:
            # 标记 API Key 错误
            if e.response.status_code in [401, 403, 429]:
                self.api_manager.mark_key_error(api_key)

            # 尝试使用下一个 API Key 重试
            if self.api_manager.get_available_count() > 0:
                return self.generate(prompt, max_tokens, temperature, stream)
            else:
                raise Exception("所有 API Key 都不可用")

        except Exception as e:
            raise Exception(f"LLM 请求失败: {e}")

    def generate_with_system(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        使用系统提示词生成

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            max_tokens: 最大 token 数
            temperature: 温度参数

        Returns:
            生成的文本
        """
        api_key = self.get_api_key()

        headers = {
            "x-api-key": api_key.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        data = {
            "model": api_key.model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": temperature,
        }

        try:
            response = requests.post(
                f"{api_key.base_url}/v1/messages",
                headers=headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()

            if "content" in result and len(result["content"]) > 0:
                return result["content"][0].get("text", "")
            return ""

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403, 429]:
                self.api_manager.mark_key_error(api_key)

            if self.api_manager.get_available_count() > 0:
                return self.generate_with_system(
                    system_prompt, user_prompt, max_tokens, temperature
                )
            else:
                raise Exception("所有 API Key 都不可用")

        except Exception as e:
            raise Exception(f"LLM 请求失败: {e}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        多轮对话

        Args:
            messages: 消息列表
            max_tokens: 最大 token 数
            temperature: 温度参数

        Returns:
            生成的文本
        """
        api_key = self.get_api_key()

        headers = {
            "x-api-key": api_key.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        data = {
            "model": api_key.model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                f"{api_key.base_url}/v1/messages",
                headers=headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()

            if "content" in result and len(result["content"]) > 0:
                return result["content"][0].get("text", "")
            return ""

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403, 429]:
                self.api_manager.mark_key_error(api_key)

            if self.api_manager.get_available_count() > 0:
                return self.chat(messages, max_tokens, temperature)
            else:
                raise Exception("所有 API Key 都不可用")

        except Exception as e:
            raise Exception(f"LLM 请求失败: {e}")
