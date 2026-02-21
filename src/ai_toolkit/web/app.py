"""
AI Toolkit Web API
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from ai_toolkit.core.config import get_config
from ai_toolkit.core.api_manager import get_api_manager
from ai_toolkit.core.llm_client import LLMClient

app = FastAPI(title="AI Toolkit API", version="0.3.0")


# 数据模型
class GenerateRequest(BaseModel):
    prompt: str
    provider: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7


class GenerateResponse(BaseModel):
    text: str
    provider: str
    model: str


# 路由
@app.get("/")
async def root():
    """首页"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Toolkit</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }
            h1 { color: #333; }
            .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>🤖 AI Toolkit Web UI</h1>
        <div class="card">
            <h2>功能</h2>
            <ul>
                <li><a href="/docs">API 文档</a></li>
                <li><a href="/status">系统状态</a></li>
                <li><a href="/generate">代码生成</a></li>
            </ul>
        </div>
    </body>
    </html>
    """)


@app.get("/status")
async def status():
    """系统状态"""
    config = get_config()
    api_manager = get_api_manager()

    status_info = {
        "version": "0.3.0",
        "config": {
            "ollama_base_url": config.ollama_base_url,
            "data_dir": str(config.data_dir),
        },
        "api_keys": {
            "total": api_manager.get_total_count(),
            "available": api_manager.get_available_count(),
            "status": api_manager.get_status(),
        },
    }

    return JSONResponse(status_info)


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """生成代码"""
    try:
        client = LLMClient(provider=request.provider)

        system_prompt = """你是一个专业的程序员助手。
请根据用户的需求生成高质量的代码。
只输出代码，不要有其他解释。"""

        code = client.generate_with_system(
            system_prompt=system_prompt,
            user_prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        api_key = client.current_key

        return GenerateResponse(
            text=code,
            provider=api_key.provider,
            model=api_key.model,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    启动Web服务器

    Args:
        host: 主机地址
        port: 端口号
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
