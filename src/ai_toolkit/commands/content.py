"""
内容管理系统
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import json

console = Console()


@click.group(name="content")
def content_cli():
    """内容管理和营销"""
    pass


@content_cli.command(name="blog")
@click.option("--title", "-t", help="标题")
@click.option("--topic", help="主题")
def create_blog(title: str, topic: str):
    """创建技术博客"""
    console.print("\n📝 创建技术博客\n")

    if title:
        console.print(f"标题: {title}")
    else:
        title = "AI Toolkit v0.3.0 - 架构设计与最佳实践"

    if topic:
        console.print(f"主题: {topic}")

    # 博客模板
    blog_template = f"""# {title}

> 作者: David | 日期: {datetime.now().strftime('%Y-%m-%d')}

## 简介

AI Toolkit 是一个强大的本地AI工具箱，让AI开发更简单。本文介绍其架构设计和最佳实践。

## 核心功能

### 1. AI编码助手
- 10个API Key自动轮换
- 支持4个LLM提供商
- 代码生成、审查、解释

### 2. 插件系统
- 动态加载/卸载
- 可扩展架构
- 命令拦截

### 3. RAG知识库
- 向量检索
- 智能匹配
- 高效存储

## 架构设计

```
ai-toolkit/
├── src/ai_toolkit/
│   ├── commands/     # 命令实现
│   ├── core/         # 核心功能
│   └── utils/        # 工具函数
└── tests/            # 测试用例
```

## 最佳实践

### 1. API Key管理
```bash
export BIGMODEL_API_KEY="your_key"
export MINIMAX_API_KEY="your_key"
```

### 2. 插件开发
```python
# 自定义插件
from ai_toolkit.core.plugin import Plugin

class MyPlugin(Plugin):
    def on_load(self):
        print("插件已加载")
```

### 3. RAG使用
```bash
ai-toolkit rag create my-knowledge
ai-toolkit rag query my-knowledge "问题"
```

## 性能优化

- 异步I/O提升性能
- 缓存机制减少调用
- 连接池管理资源

## 总结

AI Toolkit 提供了完整的本地AI开发工具链，让AI开发更简单高效。

GitHub: https://github.com/flowerjunjie/ai-toolkit
"""

    # 保存博客
    content_dir = Path.home() / ".ai-toolkit" / "content" / "blog"
    content_dir.mkdir(parents=True, exist_ok=True)

    blog_file = content_dir / f"{datetime.now().strftime('%Y%m%d')}-{title.replace(' ', '-')}.md"

    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_template)

    console.print(f"\n✅ 博客已创建: {blog_file}")
    console.print("\n💡 发布建议:")
    console.print("1. 掘金技术社区")
    console.print("2. CSDN博客")
    console.print("3. 知乎专栏")
    console.print("4. 个人博客")


@content_cli.command(name="video")
@click.option("--topic", "-t", help="视频主题")
@click.option("--duration", "-d", help="视频时长")
def create_video(topic: str, duration: str):
    """创建视频脚本"""
    console.print("\n🎬 创建视频脚本\n")

    if not topic:
        topic = "AI Toolkit 快速开始"

    if not duration:
        duration = "10分钟"

    # 视频脚本模板
    script_template = f"""# AI Toolkit 视频脚本

## 主题: {topic}
## 时长: {duration}

### 开场 (30秒)
"大家好，今天介绍AI Toolkit - 一个强大的本地AI工具箱。"

### 演示 (8分钟)
1. 安装: pip install ai-toolkit
2. 初始化: ai-toolkit init
3. 下载模型: ai-toolkit models pull llama3.2
4. AI编码: ai-toolkit coding generate "写一个快速排序"
5. Web UI: ai-toolkit webui

### 高级功能 (1分钟)
- 插件系统
- RAG知识库
- 任务调度
- 系统监控

### 结尾 (30秒)
"AI Toolkit 让AI开发更简单。GitHub链接在评论区。"

## 录制建议
- 使用OBS Studio
- 添加字幕
- 配合演示
- 控制时长
"""

    # 保存脚本
    content_dir = Path.home() / ".ai-toolkit" / "content" / "video"
    content_dir.mkdir(parents=True, exist_ok=True)

    script_file = content_dir / f"{datetime.now().strftime('%Y%m%d')}-{topic.replace(' ', '-')}.md"

    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_template)

    console.print(f"\n✅ 视频脚本已创建: {script_file}")
    console.print("\n💡 发布建议:")
    console.print("1. B站: https://bilibili.com")
    console.print("2. YouTube: https://youtube.com")
    console.print("3. 抖音: 快速教程")
    console.print("4. 视频号: 微信生态")


@content_cli.command(name="tutorial")
@click.option("--level", "-l", type=click.Choice(["beginner", "intermediate", "advanced"]), help="难度级别")
@click.option("--topic", "-t", help="教程主题")
def create_tutorial(level: str, topic: str):
    """创建教程"""
    console.print("\n📚 创建教程\n")

    if not level:
        level = "beginner"

    if not topic:
        topic = "AI Toolkit 入门教程"

    # 教程模板
    tutorial_template = f"""# {topic}

> 难度: {level.capitalize()} | 预计时间: 30分钟

## 前置要求

- Python 3.8+
- Ollama (用于本地模型)
- 基础命令行知识

## 第一步: 安装

\`\`\`bash
pip install ai-toolkit
\`\`\`

## 第二步: 初始化

\`\`\`bash
ai-toolkit init
\`\`\`

## 第三步: 下载模型

\`\`\`bash
ai-toolkit models pull llama3.2
\`\`\`

## 第四步: 运行模型

\`\`\`bash
ai-toolkit models run llama3.2 "你好"
\`\`\`

## 第五步: AI编码

\`\`\`bash
ai-toolkit coding generate "用Python写一个快速排序"
\`\`\`

## 进阶功能

### RAG知识库
\`\`\`bash
ai-toolkit rag create my-knowledge
ai-toolkit rag query my-knowledge "问题"
\`\`\`

### Web UI
\`\`\`bash
ai-toolkit webui
# 访问 http://localhost:8000
\`\`\`

## 总结

AI Toolkit 让AI开发更简单！

GitHub: https://github.com/flowerjunjie/ai-toolkit
"""

    # 保存教程
    content_dir = Path.home() / ".ai-toolkit" / "content" / "tutorial"
    content_dir.mkdir(parents=True, exist_ok=True)

    tutorial_file = content_dir / f"{datetime.now().strftime('%Y%m%d')}-{topic.replace(' ', '-')}.md"

    with open(tutorial_file, "w", encoding="utf-8") as f:
        f.write(tutorial_template)

    console.print(f"\n✅ 教程已创建: {tutorial_file}")
    console.print("\n💡 发布建议:")
    console.print("1. 官方文档")
    console.print("2. GitHub README")
    console.print("3. 技术社区")
    console.print("4. 视频描述")


@content_cli.command(name="calendar")
def show_calendar():
    """显示内容日历"""
    console.print("\n📆 内容日历\n")

    calendar = [
        ("周一", "技术博客", "架构设计", "掘金/CSDN"),
        ("周二", "视频教程", "快速开始", "B站/YouTube"),
        ("周三", "使用案例", "最佳实践", "知乎/简书"),
        ("周四", "功能演示", "Web UI", "视频号"),
        ("周五", "开发日志", "迭代更新", "Twitter/Mastodon"),
    ]

    table = Table(show_header=True)
    table.add_column("日期", style="cyan")
    table.add_column("类型", style="green")
    table.add_column("主题", style="yellow")
    table.add_column("平台", style="blue")

    for day, content_type, topic, platform in calendar:
        table.add_row(day, content_type, topic, platform)

    console.print(table)

    console.print("\n💡 内容策略:")
    console.print("1. 保持一致性")
    console.print("2. 提供价值")
    console.print("3. 多平台分发")
    console.print("4. 互动反馈")


@content_cli.command(name="list")
def list_content():
    """列出所有内容"""
    console.print("\n📋 内容列表\n")

    content_dir = Path.home() / ".ai-toolkit" / "content"

    if not content_dir.exists():
        console.print("[yellow]暂无内容[/yellow]")
        return

    # 统计各类内容
    for category in ["blog", "video", "tutorial"]:
        category_dir = content_dir / category
        if category_dir.exists():
            files = list(category_dir.glob("*.md"))
            console.print(f"[cyan]{category.capitalize()}:[/cyan] {len(files)} 篇")


@content_cli.command(name="ideas")
def show_ideas():
    """内容创意"""
    console.print("\n💡 内容创意\n")

    ideas = [
        ("AI Toolkit vs 其他工具", "对比文章"),
        ("10个实用技巧", "技巧文章"),
        ("插件开发指南", "教程"),
        ("性能优化实战", "案例"),
        ("企业级应用", "案例"),
        ("未来路线图", "文章"),
        ("用户故事", "案例"),
        ("最佳实践", "指南"),
    ]

    table = Table(show_header=True)
    table.add_column("主题", style="cyan")
    table.add_column("类型", style="green")

    for idea, type_ in ideas:
        table.add_row(idea, type_)

    console.print(table)

    console.print("\n💡 创意来源:")
    console.print("1. 用户反馈")
    console.print("2. 社区讨论")
    console.print("3. 行业趋势")
    console.print("4. 竞品分析")
