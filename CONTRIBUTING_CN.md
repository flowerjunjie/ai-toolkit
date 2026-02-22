# AI Toolkit - 贡献指南 🤝

## 如何贡献

欢迎贡献AI Toolkit！我们感谢所有形式的贡献。

---

## 🎯 贡献类型

### 1. 报告Bug
- 发现Bug？请创建Issue
- 提供重现步骤
- 附上日志和错误信息

### 2. 建议新功能
- 有好想法？请创建Issue
- 说明使用场景
- 讨论实现方案

### 3. 提交代码
- 修复Bug
- 添加新功能
- 改进文档
- 优化性能

### 4. 改进文档
- 修正错误
- 补充示例
- 翻译文档
- 改进表达

### 5. 帮助他人
- 回答Issue
- 帮助新手
- 分享经验
- 推广项目

---

## 🛠️ 开发环境设置

### Fork和Clone
```bash
# 1. Fork项目
# https://github.com/flowerjunjie/ai-toolkit

# 2. Clone你的Fork
git clone https://github.com/YOUR_USERNAME/ai-toolkit.git
cd ai-toolkit

# 3. 添加上游仓库
git remote add upstream https://github.com/flowerjunjie/ai-toolkit.git
```

### 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -e ".[dev]"
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_models.py

# 查看覆盖率
pytest --cov=ai_toolkit
```

### 代码格式化
```bash
# 格式化代码
black ai_toolkit/
isort ai_toolkit/

# 检查代码风格
flake8 ai_toolkit/

# 类型检查
mypy ai_toolkit/
```

---

## 📝 提交PR流程

### 1. 创建分支
```bash
# 从main创建分支
git checkout main
git pull upstream main

# 创建特性分支
git checkout -b feature/your-feature-name
```

### 2. 进行修改
```bash
# 添加你的代码
git add .

# 提交
git commit -m "feat: add your feature description"
```

### 3. 推送分支
```bash
# 推送到你的Fork
git push origin feature/your-feature-name
```

### 4. 创建PR
- 访问 GitHub
- 点击 "New Pull Request"
- 填写PR模板
- 等待review

---

## 🎨 代码规范

### Python风格
- 遵循PEP 8
- 使用类型提示
- 添加文档字符串
- 编写单元测试

### 提交信息
使用约定式提交：
```
feat: 添加新功能
fix: 修复Bug
docs: 更新文档
style: 代码格式
refactor: 重构代码
perf: 性能优化
test: 添加测试
chore: 构建/工具
```

### 代码示例
```python
from typing import Optional

def greet(name: str, enthusiastic: bool = False) -> str:
    """
    向用户问好
    
    Args:
        name: 用户名
        enthusiastic: 是否热情
    
    Returns:
        问候语
    """
    message = f"Hello, {name}!"
    if enthusiastic:
        message += " How are you?"
    return message
```

---

## 🧪 测试指南

### 单元测试
```python
# tests/test_models.py
import pytest
from ai_toolkit.core.models import ModelManager

def test_model_pull():
    """测试模型拉取"""
    manager = ModelManager()
    result = manager.pull("llama2")
    assert result.success

def test_model_run():
    """测试模型运行"""
    manager = ModelManager()
    result = manager.run("llama2", "test")
    assert result.text
```

### 集成测试
```python
# tests/integration/test_rag.py
def test_rag_workflow():
    """测试RAG工作流"""
    # 创建知识库
    rag = RAG.create("test", "./docs")
    
    # 搜索
    results = rag.search("test query")
    
    # 断言
    assert len(results) > 0
```

### 性能测试
```python
# tests/perf/test_benchmark.py
def test_inference_speed():
    """测试推理速度"""
    start = time.time()
    model.run("llama2", "test")
    elapsed = time.time() - start
    
    # 应该在1秒内完成
    assert elapsed < 1.0
```

---

## 📖 文档贡献

### 改进文档
```bash
# 1. Fork项目
# 2. 编辑文档
# 3. 提交PR
```

### 文档结构
```
docs/
├── README.md           # 总览
├── installation.md     # 安装指南
├── quickstart.md       # 快速开始
├── api/               # API文档
│   ├── models.md
│   ├── rag.md
│   └── coding.md
└── guides/            # 指南
    ├── deployment.md
    └── optimization.md
```

### 文档风格
- 使用清晰的标题
- 提供代码示例
- 添加截图/图表
- 保持简洁明了

---

## 🐛 Bug报告

### Bug报告模板
```markdown
### 描述
简要描述Bug

### 复现步骤
1. 步骤1
2. 步骤2
3. 步骤3

### 期望行为
应该发生什么

### 实际行为
实际发生了什么

### 环境
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.11.0]
- AI Toolkit: [e.g. 0.3.0]

### 日志
```
[日志输出]
```
```

---

## 💡 功能建议

### 功能建议模板
```markdown
### 问题
当前存在的问题或痛点

### 建议
详细描述你的建议

### 优势
这个建议的优势

### 替代方案
考虑过的替代方案

### 示例
使用示例或伪代码
```

---

## 🌍 国际化

### 翻译文档
```bash
# 1. 创建语言目录
mkdir docs/zh

# 2. 翻译文档
cp README.md docs/zh/README.md
# 编辑 docs/zh/README.md

# 3. 提交PR
```

### 支持的语言
- English ✅
- 中文（简体）✅
- 中文（繁体）- 欢迎
- 日本語 - 欢迎
- Español - 欢迎

---

## 🎨 设计贡献

### Logo和图标
- 设计Logo
- 创建图标
- 制作Banner

### 截图和演示
- 录制演示视频
- 创建截图
- 制作GIF

---

## 📢 推广贡献

### 写博客
- 分享使用经验
- 教程文章
- 技术解析

### 社交媒体
- Twitter分享
- LinkedIn发布
- Reddit讨论

### 会议演讲
- 提交演讲提案
- 组织meetup
- 参与讨论

---

## 🤝 社区准则

### 我们的承诺
- 尊重所有贡献者
- 欢迎不同观点
- 建设性反馈
- 协作优先

### 不可接受
- 骚扰
- 歧视性语言
- 人身攻击
- 恶意行为

---

## 🏆 贡献者

### 核心团队
- **@flowerjunjie** - 创始人

### 贡献者
感谢所有贡献者！

查看完整贡献者列表：https://github.com/flowerjunjie/ai-toolkit/graphs/contributors

---

## 📧 联系我们

### 问题？
- 📖 文档: https://docs.ai-toolkit.dev
- 💬 Discord: https://discord.gg/ai-toolkit
- 📧 邮件: support@ai-toolkit.dev

### 紧急问题？
- 创建Issue
- 发送邮件
- Discord私信

---

## 🎉 感谢贡献

感谢你考虑为AI Toolkit做出贡献！

每一个贡献都很重要，无论是：
- 修复一个错别字
- 添加一个功能
- 回答一个问题
- 分享项目

**让我们一起让AI Toolkit变得更好！** 🚀

---

**🤝 贡献指南已完成！**

**💡 准备好贡献了吗？从现在开始！**
