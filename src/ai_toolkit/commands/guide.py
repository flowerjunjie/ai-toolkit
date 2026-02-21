"""
快速开始指南生成器
"""

import click
from pathlib import Path
from rich.console import Console

console = Console()


@click.command()
@click.option("--output", "-o", type=click.Path(), help="输出文件")
def quickstart(output: str):
    """生成快速开始指南"""
    from ai_toolkit.core.config import get_config

    config = get_config()

    guide = """# 🚀 AI Toolkit 快速开始指南

欢迎使用 AI Toolkit - 你的本地AI工具箱！

## 📦 安装

\`\`\`bash
pip install ai-toolkit
\`\`\`

## 🎯 第一次使用

### 1. 初始化
\`\`\`bash
ai-toolkit init
\`\`\`

### 2. 下载模型
\`\`\`bash
# 查看可用模型
ai-toolkit models list

# 下载一个模型（例如 llama3.2）
ai-toolkit models pull llama3.2

# 运行模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"
\`\`\`

## 💡 核心功能

### 1. Prompt模板管理

\`\`\`bash
# 添加常用Prompt
ai-toolkit prompts add python-expert "你是一个专业的Python开发者。请回答: {question}"

# 使用模板
ai-toolkit prompts run python-expert --vars question="如何优化代码？"
\`\`\`

### 2. RAG知识库

\`\`\`bash
# 创建知识库
ai-toolkit rag2 create ./docs --name my-kb

# 查询知识库
ai-toolkit rag2 query my-kb "什么是AI？"
\`\`\`

### 3. AI编码助手

\`\`\`bash
# 生成代码
ai-toolkit coding generate "用Python写一个快速排序"

# 代码审查
ai-toolkit coding review my_script.py

# 查看API状态
ai-toolkit coding status
\`\`\`

### 4. Web UI

\`\`\`bash
ai-toolkit webui
# 访问 http://localhost:8000
\`\`\`

## 📚 更多功能

### 插件系统
\`\`\`bash
# 列出插件
ai-toolkit plugin list

# 创建插件
ai-toolkit plugin create myplugin
\`\`\`

### 批处理
\`\`\`bash
# 创建批处理文件
cat > batch.txt
ai-toolkit models list
ai-toolkit prompts list

# 执行
ai-toolkit batch batch.txt
\`\`\`

### 任务调度
\`\`\`bash
# 添加定时任务（每小时备份配置）
ai-toolkit schedule add backup 1 "ai-toolkit config export backup.json"

# 启动调度器
ai-toolkit schedule start --daemon
\`\`\`

### 系统监控
\`\`\`bash
# 查看系统状态
ai-toolkit monitor status

# 实时监控
ai-toolkit monitor top
\`\`\`

## 🛠️ 进阶使用

### 命令别名
\`\`\`bash
# 创建别名
ai-toolkit alias add ls "ai-toolkit models list"

# 运行别名
ai-toolkit alias run ls
\`\`\`

### 配置管理
\`\`\`bash
# 显示配置
ai-toolkit config show

# 导出配置
ai-toolkit config export my-config.json

# 导入配置
ai-toolkit config import my-config.json
\`\`\`

## 📖 文档

- 完整文档: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- 架构文档: https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/architecture.md
- 开发指南: https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/setup-guide.md

## 🤝 支持

- 问题反馈: https://github.com/flowerjunjie/ai-toolkit/issues
- 赞助赞助: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

**开始使用吧！** 🎉
"""

    if output:
        output_path = Path(output)
    else:
        output_path = Path.cwd() / "QUICKSTART.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(guide)

    console.print(f"✅ 快速开始指南已生成: {output_path}")


@click.command()
def examples():
    """显示使用示例"""
    console.print("\n💡 使用示例\n")

    examples = [
        ("模型管理", [
            "ai-toolkit models list",
            "ai-toolkit models pull llama3.2",
            "ai-toolkit models run llama3.2 '你好'",
        ]),
        ("Prompt模板", [
            "ai-toolkit prompts add expert '你是一个{角色}'",
            "ai-toolkit prompts run expert --vars 角色=医生",
        ]),
        ("RAG知识库", [
            "ai-toolkit rag2 create ./docs --name kb",
            "ai-toolkit rag2 query kb '什么是AI？'",
        ]),
        ("AI编码", [
            "ai-toolkit coding generate '写一个快速排序'",
            "ai-toolkit coding review main.py",
            "ai-toolkit coding status",
        ]),
        ("Web UI", [
            "ai-toolkit webui",
        ]),
        ("插件", [
            "ai-toolkit plugin list",
            "ai-toolkit plugin create demo",
            "ai-toolkit plugin reload",
        ]),
        ("批处理", [
            "ai-toolkit batch commands.txt",
        ]),
        ("监控", [
            "ai-toolkit monitor status",
            "ai-toolkit monitor health",
        ]),
    ]

    from rich.table import Table

    for category, cmds in examples:
        console.print(f"\n{category}:")
        for cmd in cmds:
            console.print(f"  {cmd}")

    console.print("\n💡 输入 'ai-toolkit --help' 查看所有命令")
