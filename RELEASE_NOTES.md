# AI Toolkit v0.2.0 发布说明

## 🎉 重大更新

AI Toolkit v0.2.0 带来了更好的用户体验和强大的新功能！

### ✨ 新功能

#### 🎯 交互式初始化向导
首次使用？运行 `ai-toolkit init`，让我们引导你完成配置：
- 自动检测 Ollama 连接
- 友好的配置向导
- 一键生成配置文件

#### ⚡ 命令自动补全
再也不用记完整命令了！
- Bash 自动补全：`source <(ai-toolkit --completion)`
- Zsh 自动补全：`source <(ai-toolkit --completion-zsh)`
- 智能提示所有子命令

#### 🔄 版本检查和升级
保持最新版本：
```bash
ai-toolkit upgrade
```

#### 🛠️ 强大的工具函数库
开发者友好的底层工具：
- 连接检查和重试机制
- 带进度条的文件下载
- JSON 配置管理
- 文件备份和删除

### 📚 完整路线图
我们公开了完整的开发路线图，包括：
- v0.3.0: 真正的向量检索 RAG
- v0.4.0: 企业功能和团队协作
- v1.0.0: 生产就绪稳定版

### 🐛 Bug 修复
- 修复了 CLI 命令冲突
- 优化了错误提示
- 改进了配置管理

### 📖 文档改进
- 添加了开发路线图
- 完善了使用示例
- 更新了贡献指南

---

## 🚀 快速开始

```bash
# 安装
pip install ai-toolkit

# 初始化（新功能！）
ai-toolkit init

# 启用自动补全（新功能！）
source <(ai-toolkit --completion)

# 检查更新（新功能！）
ai-toolkit upgrade

# 下载模型
ai-toolkit models pull llama3.2

# 运行模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"
```

---

## 💡 主要功能

### 🤖 模型管理
```bash
ai-toolkit models list          # 列出模型
ai-toolkit models pull <name>   # 下载模型
ai-toolkit models run <name>    # 运行模型
ai-toolkit models delete <name> # 删除模型
ai-toolkit models info <name>   # 模型信息
```

### 📝 Prompt 模板
```bash
ai-toolkit prompts list                      # 列出模板
ai-toolkit prompts add <name> <content>      # 添加模板
ai-toolkit prompts run <name> --vars k=v     # 运行模板
ai-toolkit prompts show <name>               # 查看模板
```

### 🚀 RAG 知识库
```bash
ai-toolkit rag create <path> --name <kb>     # 创建知识库
ai-toolkit rag query <kb> "question"         # 查询知识库
ai-toolkit rag list                          # 列出知识库
```

### 🧪 性能测试
```bash
ai-toolkit benchmark run --model <name>      # 运行测试
ai-toolkit benchmark compare m1 m2           # 对比模型
```

---

## 📊 技术栈

- Python 3.8+
- Click (CLI 框架)
- Rich (终端美化)
- Pydantic (配置管理)
- Requests (HTTP 客户端)
- Ollama API (模型运行)

---

## 🔗 链接

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **PyPI**: https://pypi.org/project/ai-toolkit/
- **文档**: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- **路线图**: https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/ROADMAP.md

---

## 🙏 致谢

感谢所有贡献者和用户的反馈！

---

## 📅 下一个版本 (v0.3.0)

计划功能：
- 真正的向量检索 RAG (ChromaDB)
- 多模型支持 (LM Studio, LocalAI)
- 插件系统
- Web UI

**敬请期待！** 🚀

---

**下载**: `pip install --upgrade ai-toolkit`
**GitHub**: https://github.com/flowerjunjie/ai-toolkit
