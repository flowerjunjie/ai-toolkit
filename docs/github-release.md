# 🎉 AI Toolkit v0.2.0 - 交互式初始化和自动补全

## 📢 重大更新

AI Toolkit v0.2.0 带来了更好的用户体验和强大的新功能！

### ✨ 新功能

#### 🎯 交互式初始化向导
首次使用？运行 `ai-toolkit init`，让我们引导你完成配置：
- ✅ 自动检测 Ollama 连接
- ✅ 友好的配置向导
- ✅ 一键生成配置文件

#### ⚡ 命令自动补全
再也不用记完整命令了！
- ✅ Bash 自动补全：`source <(ai-toolkit --completion)`
- ✅ Zsh 自动补全：`source <(ai-toolkit --completion-zsh)`
- ✅ 智能提示所有子命令

#### 🔄 版本检查和升级
保持最新版本：
```bash
ai-toolkit upgrade
```

#### 🛠️ 强大的工具函数库
开发者友好的底层工具：
- ✅ 连接检查和重试机制
- ✅ 带进度条的文件下载
- ✅ JSON 配置管理
- ✅ 文件备份和删除

#### ☕️ 赞助支持
如果你觉得这个项目有帮助，欢迎请我喝杯咖啡！
- ✅ 微信赞赏
- ✅ GitHub Sponsor
- ✅ 详见 [SPONSORSHIP.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md)

### 📚 文档完善
- ✅ 开发路线图 (v0.3.0 - v1.0.0)
- ✅ 完整的使用示例
- ✅ 贡献指南
- ✅ 发布说明

### 🐛 Bug 修复
- ✅ 修复了 CLI 命令冲突
- ✅ 优化了错误提示
- ✅ 改进了配置管理

---

## 🚀 快速开始

### 安装

```bash
pip install ai-toolkit
```

### 初始化（新功能！）

```bash
ai-toolkit init
```

### 启用自动补全（新功能！）

```bash
# Bash
source <(ai-toolkit --completion)

# Zsh
source <(ai-toolkit --completion-zsh)
```

### 基本使用

```bash
# 下载模型
ai-toolkit models pull llama3.2

# 运行模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"

# 创建 Prompt 模板
ai-toolkit prompts add expert "你是一个专业的{角色}"

# 使用模板
ai-toolkit prompts run expert --vars 角色="Python开发者"

# 创建 RAG 知识库
ai-toolkit rag create ./docs --name my-kb

# 查询知识库
ai-toolkit rag query my-kb "什么是AI？"

# 性能测试
ai-toolkit benchmark run --model llama3.2
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
ai-toolkit prompts edit <name> <content>     # 编辑模板
ai-toolkit prompts delete <name>             # 删除模板
```

### 🚀 RAG 知识库
```bash
ai-toolkit rag create <path> --name <kb>     # 创建知识库
ai-toolkit rag query <kb> "question"         # 查询知识库
ai-toolkit rag list                          # 列出知识库
ai-toolkit rag delete <kb>                   # 删除知识库
```

### 🧪 性能测试
```bash
ai-toolkit benchmark run --model <name>      # 运行测试
ai-toolkit benchmark compare m1 m2           # 对比模型
```

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click (CLI), Rich (终端美化)
- **库**: Pydantic (配置管理), Requests (HTTP)
- **平台**: Ollama API
- **测试**: pytest, black, flake8, mypy

---

## 🔗 链接

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **文档**: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md
- **路线图**: https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/ROADMAP.md

---

## 📦 完整变更

### 新增
- 交互式初始化向导 (`ai-toolkit init`)
- 命令自动补全支持 (Bash/Zsh)
- 版本检查和升级功能 (`ai-toolkit upgrade`)
- 工具函数库 (helpers.py)
- 开发路线图 (ROADMAP.md)
- 赞助支持 (SPONSORSHIP.md)

### 优化
- CLI 命令结构优化
- 错误处理改进
- 配置管理增强
- 文档完善

### 修复
- 修复 CLI 命令冲突
- 修复配置文件处理问题

---

## 🙏 致谢

感谢所有贡献者和用户的反馈！

---

## 📅 下一个版本 (v0.3.0)

计划功能：
- 🎯 真正的向量检索 RAG (ChromaDB)
- 🤖 多模型支持 (LM Studio, LocalAI)
- 🔌 插件系统
- 🌐 Web UI

**敬请期待！** 🚀

---

**下载**: `pip install --upgrade ai-toolkit`
**GitHub**: https://github.com/flowerjunjie/ai-toolkit
**⭐️ 如果这个项目对你有帮助，请给个 Star 支持一下！**
