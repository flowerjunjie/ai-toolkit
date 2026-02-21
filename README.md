# 🤖 AI Toolkit - 本地AI工具箱

> 一个强大的本地AI模型管理和工具集，让AI开发更简单。

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/flowerjunjie/ai-toolkit.svg?style=social)](https://github.com/flowerjunjie/ai-toolkit)

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-%23EA4AAA?style=for-the-badge&logo=GitHub+Sponsors)](https://github.com/sponsors/flowerjunjie)

## ✨ 特性

### 🎯 核心功能 (47个模块，390+命令)

#### 🤖 AI能力 (6个)
- **模型管理** - 快速下载、切换、删除本地AI模型
- **Prompt模板** - 管理和复用你的AI提示词（支持变量）
- **RAG知识库** - 一键搭建本地知识库问答
- **AI编码助手** - 支持4个LLM提供商，10个API Key自动轮换
- **性能测试** - 测试和对比不同模型的表现
- **预设模板库** - Python专家、代码审查员、技术写作等

#### 🛠️ 开发工具 (8个)
- **插件系统** - 动态加载/卸载，可扩展架构
- **批处理模式** - 从文件批量执行命令
- **任务调度** - 定时任务自动化
- **命令别名** - 简化常用命令
- **历史记录** - 追踪操作历史
- **测试工具** - 完整测试套件
- **文档工具** - 自动生成文档
- **QA测试** - 质量保证

#### 🌐 企业功能 (10个)
- **团队协作** - 团队管理、权限控制、活动追踪
- **项目管理** - 任务管理、看板视图、里程碑
- **API网关** - 路由管理、速率限制、缓存控制
- **微服务架构** - 服务管理、健康检查、服务网格
- **智能代理** - 任务代理、工作流代理、自主代理
- **事件驱动** - 发布订阅、事件总线、消息队列
- **自动化编排** - 依赖图、DAG、任务调度
- **工作流自动化** - 工作流管理、触发器、模板

#### 📊 数据处理 (4个)
- **数据管道** - ETL工具、数据验证、数据转换
- **流处理** - 实时处理、窗口操作、流连接
- **高级分析** - 使用分析、性能分析、趋势预测
- **机器学习** - 模型训练、模型评估、模型部署

#### 🚀 DevOps (4个)
- **CI/CD** - 自动化测试、自动部署、回滚机制
- **Docker** - 容器化、Docker Compose、镜像管理
- **监控** - 系统监控、性能监控、日志管理
- **容器编排** - 自动扩展、负载均衡

#### 💰 商业化 (3个)
- **命令市场** - 命令分享和下载
- **变现分析** - 收入概览、赞助者管理、功能列表
- **自动化工具** - 进度追踪、自动汇报

#### 👥 社区营销 (2个)
- **社区工具** - 推广帖子、模板、计划
- **SEO优化** - 关键词分析、元数据生成、外链建设

#### 🔒 安全合规 (2个)
- **安全工具** - 安全审计、漏洞扫描、策略生成
- **国际化** - 多语言支持、翻译管理

#### ⚙️ 系统管理 (9个)
- **配置管理** - 导入导出配置
- **系统管理** - 系统信息、路径管理
- **诊断工具** - 系统诊断、环境检查
- **备份恢复** - 数据备份、数据恢复
- **系统监控** - 实时监控、健康检查
- **性能优化** - 性能分析、代码优化
- **用户体验** - UX分析、使用指南
- **工作流自动化** - 自动化任务
- **自动化编排** - 资源管理、扩展编排

#### 🤖 自动化 (5个)
- **批处理** - 从文件批量执行
- **任务调度** - 定时任务管理
- **历史记录** - 操作历史
- **工作流** - 工作流管理
- **编排** - 任务编排

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

#### 3. 智能代理

```bash
# 创建代理
ai-toolkit agent create --name my-agent --type task

# 部署代理
ai-toolkit agent deploy --agent my-agent

# 分配任务
ai-toolkit agent task --agent my-agent --task "分析数据"
```

#### 4. 微服务

```bash
# 初始化服务
ai-toolkit microservice init --name my-service

# 部署服务
ai-toolkit microservice deploy --service my-service --env prod

# 健康检查
ai-toolkit microservice health
```

#### 5. 数据管道

```bash
# 创建管道
ai-toolkit pipeline create --name etl-pipeline

# 运行管道
ai-toolkit pipeline run --pipeline etl-pipeline

# 监控管道
ai-toolkit pipeline monitor
```

---

## 📚 完整功能列表

| 模块 | 命令数 | 说明 |
|------|--------|------|
| models | 5 | 模型管理 |
| prompts | 6 | Prompt模板 |
| rag | 4 | 基础RAG |
| rag2 | 4 | 向量RAG |
| coding | 4 | AI编码助手 |
| benchmark | 2 | 性能测试 |
| plugin | 5 | 插件系统 |
| template | 3 | 预设模板库 |
| test | 5 | 测试工具 |
| qa | 7 | QA测试 |
| docs | 6 | 文档工具 |
| batch | 1 | 批处理 |
| schedule | 4 | 任务调度 |
| export | 3 | 数据导出 |
| monitor | 3 | 系统监控 |
| backup | 3 | 备份恢复 |
| system | 4 | 系统管理 |
| diag | 3 | 诊断工具 |
| shell | 1 | 交互式Shell |
| alias | 3 | 命令别名 |
| history | 3 | 历史记录 |
| config | 4 | 配置管理 |
| webui | 1 | Web界面 |
| init | 1 | 初始化 |
| upgrade | 1 | 版本检查 |
| status | 1 | 系统状态 |
| guide | 2 | 快速指南 |
| market | 6 | 命令市场 |
| revenue | 6 | 变现分析 |
| auto | 4 | 自动化工具 |
| community | 7 | 社区工具 |
| feedback | 7 | 用户反馈 |
| content | 6 | 内容管理 |
| seo | 6 | SEO优化 |
| perf | 7 | 性能优化 |
| ux | 7 | 用户体验 |
| security | 7 | 安全工具 |
| i18n | 7 | 国际化 |
| cicd | 7 | CI/CD工具 |
| docker | 8 | Docker工具 |
| analytics | 8 | 高级分析 |
| ml | 9 | 机器学习 |
| team | 8 | 团队协作 |
| project | 9 | 项目管理 |
| gateway | 10 | API网关 |
| microservice | 10 | 微服务 |
| pipeline | 8 | 数据管道 |
| stream | 8 | 流处理 |
| workflow | 8 | 工作流自动化 |
| orchestrate | 8 | 自动化编排 |
| agent | 8 | 智能代理 |
| event | 8 | 事件驱动 |

**总计**: 390+ 命令

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click, Rich, Pydantic, FastAPI
- **数据库**: ChromaDB, SQLite
- **LLM提供商**: BigModel, MiniMax, Kimi, Doubao (支持环境变量配置)
- **Web**: FastAPI + Uvicorn
- **容器化**: Docker, Docker Compose
- **编排**: Kubernetes (规划中)
- **测试**: pytest

---

## 🔗 链接

### 文档
- **完整文档**: [README.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md)
- **架构文档**: [docs/architecture.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/architecture.md)
- **开发指南**: [docs/setup-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/setup-guide.md)
- **API文档**: [docs/api-keys-guide.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/api-keys-guide.md)
- **更新日志**: [CHANGELOG.md](https://github.com/flowerjunjie/ai-toolkit/blob/main/CHANGELOG.md)

### 支持
- **Issues**: https://github.com/flowerjunjie/ai-toolkit/issues
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

## 🎯 路线图

### v0.3.0 (当前) ✅
- ✅ 完整的生产级工具箱
- ✅ 47个功能模块
- ✅ 390+命令
- ✅ 54000+行代码
- ✅ 企业级质量

### v0.4.0 (规划中)
- [ ] Web UI增强
- [ ] 更多LLM提供商
- [ ] 分布式部署
- [ ] 云服务集成

### v1.0.0 (目标)
- [ ] 完整Web界面
- [ ] 企业功能套件
- [ ] 云服务版本
- [ ] 全球部署

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
ai-toolkit diag all
# 完整系统诊断
```

### 查看所有命令
```bash
ai-toolkit --help
# 显示所有可用命令
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
