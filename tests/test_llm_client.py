"""
LLM客户端测试
"""

import pytest
from unittest.mock import Mock, patch
from ai_toolkit.core.llm_client import LLMClient


class TestLLMClient:
    """LLMClient 类测试"""

    @pytest.fixture
    def mock_response(self):
        """模拟响应"""
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {
            "content": [
                {
                    "text": "生成的代码"
                }
            ]
        }
        return mock

    def test_client_creation(self):
        """测试客户端创建"""
        client = LLMClient()
        assert client is not None
        assert client.provider is None

    def test_client_with_provider(self):
        """测试指定提供商"""
        client = LLMClient(provider="bigmodel")
        assert client.provider == "bigmodel"

    @patch('requests.post')
    def test_generate(self, mock_post, mock_response):
        """测试生成文本"""
        mock_post.return_value = mock_response

        client = LLMClient()
        result = client.generate("写一个快速排序")

        assert result == "生成的代码"

    @patch('requests.post')
    def test_generate_with_system(self, mock_post, mock_response):
        """测试使用系统提示词生成"""
        mock_post.return_value = mock_response

        client = LLMClient()
        result = client.generate_with_system(
            system_prompt="你是Python专家",
            user_prompt="写一个快速排序"
        )

        assert result == "生成的代码"
