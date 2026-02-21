# 🤖 AI Toolkit - 本地AI工具箱

> 一个强大的本地AI模型管理和工具集，让AI开发更简单。

[![License: MIT](https://img.shoelace.ai/assets/badges/mit.svg)](LICENSE)
[![GitHub stars](https://img.shoelace.ai/assets/badosges/github-stars.svg)](https://github.com/flowerjunjie/ai-toolkit/stars)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ 特性

### 🎯 核心功能
- 🤖 **模型管理** - 快速下载、切换、删除本地AI模型
- 📝 **Prompt模板** - 管理和复用你的AI提示词（支持变量）
- 🚀 **RAG知识库** - 一键搭建本地知识库问答
- 🧪 **性能测试** - 测试和对比不同模型的表现
- 🤖 **AI编码助手** - 多LLM提供商支持，API Key轮换
- 🔌 **插件系统** - 可扩展的插件架构
- ⚙️ **批处理** - 自动化批量执行命令
- ⏰ **任务调度** - 定时任务自动化
- 🌐 **Web UI** - 简洁的Web界面
- 📊 **系统监控** - 实时监控系统状态
- 💾 **备份恢复** - 数据安全保障

### 🛠️ 实用工具
- 📂 **配置管理** - 导入导出配置
- 🔄 **命令别名** - 简化常用命令
- 📜 **历史记录** - 追踪操作历史
- 🔍 **系统诊断** - 问题排查工具
- 🐚 **交互式Shell** - 友好的交互模式

---

## 🚀 快速开始

### 安装

```bash
pip install ai-toolkit
```

### 初始化

```bash
ai-toolkit init
```

### 核心功能演示

#### 1. 模型管理

```bash
# 下载模型
ai-toolkit models pull llama3.2

# 运行模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"

# 查看模型信息
ai-toolkit models info llama3.2
```

#### 2. Prompt 模板

```bash
# 添加模板
ai-toolkit prompts add expert "你是一个专业的{角色}"

# 使用模板
ai-toolkit prompts run expert --vars 角色="Python开发者"

# 列出所有模板
ai-toolkit prompts list
```

#### 3. RAG 知识库（向量检索）

```bash
# 创建知识库
aitoolkit rag2 create ./docs --name my-kb

# 查询知识库
ai-toolkit rag2 query my-kb "什么是AI？"

# 列出知识库
ai-toolkit rag2 list
```

#### 4. AI 编码助手

```bash
# 生成代码
ai-toolkit coding generate "用Python写一个快速排序"

# 代码审查
ai-toolkit coding review main.py

# 查看API状态
ai-toolkit coding status
```

#### 5. Web UI

```bash
ai-toolkit webui
# 访问 http://localhost:8000
```

#### 6. 插件系统

```bash
# 创建插件
ai-toolkit plugin create myplugin

# 查看插件
ai-toolkit plugin list

# 重新加载
ai-toolkit plugin reload
```

#### 7. 批处理

```bash
# 创建批处理文件
cat > commands.txt
ai-toolkit models list
ai-toolkit prompts list
ai-toolkit coding status

# 执行
ai-toolkit batch commands.txt
```

#### 8. 系统监控

```bash
# 系统状态
ai-toolkit monitor status

# 实时监控
ai-toolkit monitor top

# 健康检查
ai-toolkit monitor health
```

---

## 📚 完整功能列表

### 核心功能 (16个)
1. **models** - 模型管理 (list/pull/run/delete/info)
2. **prompts** - Prompt模板 (add/run/show/edit/delete/list)
3. **rag** - 基础RAG (create/query/list/delete)
4. **rag2** - 向量RAG (create/query/info/list)
5. **benchmark** - 性能测试 (run/compare)
6. **coding** - AI编码助手 (generate/review/explain/status)
7. **alias** - 命令别名 (add/remove/list/run)
8. **history** - 历史记录 (list/clear/stats)
9. **config** - 配置管理 (show/export/import/reset)
10. **webui** - Web UI
11. **plugin** - 插件系统 (list/load/unload/create/reload/run)
12. **batch** - 批处理
13. **schedule** - 任务调度
14. **export** - 数据导出
15. **monitor** - 系统监控
16. **backup** - 备份恢复
17. **system** - 系统管理
18. **diag** - 诊断工具
19. **shell** - 交互式Shell
20. **guide** - 快速指南

### 系统功能
- **init** - 初始化配置
- **upgrade** - 版本检查
- **status** - 系统状态

**总计**: 70+ 命令

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click, Rich, Pydantic, FastAPI
- **数据库**: ChromaDB (向量检索)
- **LLM提供商**: BigModel, MiniMax, Kimi, Doubao (10个API Key轮换)
- **Web**: FastAPI + Uvicorn
- **测试**: pytest

---

## 🔧 安装

### 方式1: pip (推荐)
```bash
pip install ai-toolkit
```

### 方式2: Docker
```bash
docker pull flowerjunjie/ai-toolkit
docker run -it flowerjunjie/ai-toolkit
```

### 方式3: 从源码
```bash
git clone https://github.com/flowerjunjie/ai-toolkit.git
cd ai-toolkit
pip install -e .
```

---

## 📖 文档

- **完整文档**: [README.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md)
- **架构文档**: [docs/architecture.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/architecture.md)
- **开发指南**: [docs/setup-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/setup-guide.md)
- **API文档**: [docs/api-keys-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/api-keys-guide.md)
- **更新日志**: [CHANGELOG.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/CHANGELOG.md)

---

## 🎯 路线图

查看 [ROADMAP.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/ROADMAP.md)

### v0.3.0 (当前) ✅
- ✅ 完整的核心功能
- ✅ 插件系统
- ✅ Web UI
- ✅ 自动化工具

### v0.4.0 (规划中)
- [ ] 更多LLM提供商
- [ ] 分布式部署
- [ ] 企业版功能

### v1.0.0 (目标)
- [ ] 生产就绪
- [ ] 企业级功能
- [   ] 云服务

---

## 💡 使用技巧

### 交互式Shell模式
```bash
ai-toolkit shell
# 进入交互式模式
```

### 查看快速示例
```bash
ai-toolkit examples
```

### 生成快速指南
```bash
ai-toolkit quickstart > QUICKSTART.md
```

### 系统诊断
```bash
ai-toolkit diag all
```

---

## 🤝 贡献

欢迎贡献！查看 [CONTRIBUTING.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](https://github.com/flowerjunjie/ai-toolkit/blob/main/LICENSE)

---

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star 支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=flowerjunjie/ai-toolkit&type=Date)](https://star-history.com/#flowerjunjie/ai-toolkit&Date)

---

**Made with ❤️ by David and BOSS**

**🚀 让AI开发更简单！**
