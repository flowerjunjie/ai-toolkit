# 🤖 AI Toolkit - 本地AI工具箱

> 一个强大的本地AI模型管理和工具集，让AI开发更简单。

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/flowerjunjie/ai-toolkit.svg?style=social)](https://github.com/flowerjunjie/ai-toolkit)

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-%23EA4AAA?style=for-the-badge&logo=GitHub+Sponsors)](https://github.com/sponsors/flowerjunjie)

## ✨ 特性

### 🎯 核心功能 (21个模块，75+命令)

#### 🤖 AI能力
- **模型管理** - 快速下载、切换、删除本地AI模型
- **Prompt模板** - 管理和复用你的AI提示词（支持变量）
- **RAG知识库** - 一键搭建本地知识库问答
- **AI编码助手** - 支持4个LLM提供商，10个API Key自动轮换
- **性能测试** - 测试和对比不同模型的表现
- **预设模板库** - Python专家、代码审查员、技术写作等

#### 🛠️ 自动化工具
- **插件系统** - 动态加载/卸载，可扩展架构
- **批处理模式** - 从文件批量执行命令
- **任务调度** - 定时任务自动化
- **命令别名** - 简化常用命令
- **历史记录** - 追踪操作历史

#### 🌐 用户界面
- **Web UI** - FastAPI服务，RESTful API
- **交互式Shell** - 友好的交互模式
- **系统监控** - 实时监控、健康检查
- **进度显示** - 优美的进度条

#### 📦 数据管理
- **备份恢复** - 数据安全保障
- **数据导出** - Prompts、RAG、统计
- **配置管理** - 导入导出配置

#### 🔧 开发工具
- **测试工具** - 完整测试套件
- **代码检查** - 自动修复
- **诊断工具** - 问题排查

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

#### 1. AI编码助手

```bash
# 生成代码
ai-toolkit coding generate "用Python写一个快速排序"

# 代码审查
ai-toolkit coding review main.py

# 查看API状态
ai-toolkit coding status
```

#### 2. 系统监控

```bash
# 系统状态
ai-toolkit monitor status

# 实时监控（类似top）
ai-toolkit monitor top

# 健康检查
ai-toolkit monitor health
```

#### 3. 插件系统

```bash
# 查看插件
ai-toolkit plugin list

# 创建插件
ai-toolkit plugin create myplugin

# 重新加载
ai-toolkit plugin reload
```

#### 4. 交互式Shell

```bash
ai-toolkit shell
# 进入交互式模式
```

---

## 📚 完整功能列表

| 模块 | 命令数 | 说明 |
|------|--------|------|
| models | 5 | 模型管理 (list/pull/run/delete/info) |
| prompts | 6 | Prompt模板 (list/add/run/show/edit/delete) |
| rag | 4 | 基础RAG (create/query/list/delete) |
| rag2 | 4 | 向量RAG (create/query/info/list) |
| coding | 4 | AI编码助手 (generate/review/explain/status) |
| benchmark | 2 | 性能测试 (run/compare) |
| plugin | 5 | 插件系统 (list/load/unload/create/reload/run) |
| template | 3 | 预设模板库 (list/use/show) |
| test | 5 | 测试工具 (all/unit/lint/fix/watch/add) |
| batch | 1 | 批处理 |
| schedule | 4 | 任务调度 (list/add/remove/start/stop/run) |
| export | 3 | 数据导出 (prompts/rag/stats/all) |
| monitor | 3 | 系统监控 (status/top/health) |
| backup | 3 | 备份恢复 (create/list/restore) |
| system | 4 | 系统管理 (info/paths/clean/version) |
| diag | 3 | 诊断工具 (all/env/test) |
| shell | 1 | 交互式Shell |
| guide | 2 | 快速指南 |
| 其他 | 6 | 初始化/升级/状态 |

**总计**: 75+ 命令

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click, Rich, Pydantic, FastAPI
- **数据库**: ChromaDB
- **LLM提供商**: BigModel, MiniMax, Kimi, Doubao (支持环境变量配置)
- **Web**: FastAPI + Uvicorn
- **测试**: pytest

---

## 🔗 链接

### 文档
- **完整文档**: [README.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md)
- **架构文档**: [docs/architecture.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/architecture.md)
- **开发指南**: [docs/setup-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/setup-guide.md)
- **API文档**: [docs/api-keys-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/api-keys-guide.md)
- **更新日志**: [CHANGELOG.md](https://github.com//flowerjunjie/ai-toolkit/blob/main/CHANGELOG.md)

### 支持
- **Issues**: https://github.com/flowerjunjie/ai-toolkit/issues
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

## 🎯 路线图

### v0.3.0 (当前) ✅
- ✅ 完整的生产级工具箱
- ✅ 21个功能模块
- ✅ 75+命令
- ✅ 企业级质量

### v0.4.0 (规划中)
- [ ] Web UI增强
- [ ] 更多LLM提供商
- [ ] 分布式部署

### v1.0.0 (目标)
- [ ] 完整Web界面
- [ ] 企业功能
- [ ] 云服务

---

## 💡 使用技巧

### 交互式Shell模式
```bash
ai-toolkit shell
# 进入交互式模式，支持命令历史和自动补全
```

### 查看快速示例
```bash
ai-toolkit examples
# 显示所有使用示例
```

### 系统诊断
```bash
ai-tool diag all
# 完整系统诊断
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
