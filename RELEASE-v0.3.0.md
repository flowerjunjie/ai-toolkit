# 🎉 AI Toolkit v0.3.0 - 生产级本地AI工具箱

## 🚀 重大更新

AI Toolkit v0.3.0 是一个**完整的生产级**本地AI工具箱！

### ✨ 新功能 (v0.2.0 → v0.3.0)

#### 🤖 AI编码助手
- 10个API Key自动轮换
- 支持4个LLM提供商
- 代码生成、审查、解释
- API状态监控

#### 🔌 插件系统
- 动态加载/卸载
- 命令拦截
- 插件模板生成
- 可扩展架构

#### 📦 批处理模式
- 从文件执行命令
- 错误处理
- 执行统计

#### ⏰ 任务调度
- 定时任务管理
- 后台运行
- 多种时间单位

#### 🌐 Web UI
- FastAPI服务
- RESTful API
- 系统监控
- 代码生成接口

#### 📊 系统监控
- 实时监控
- 健康检查
- 资源使用统计

#### 💾 数据管理
- 备份恢复
- 数据导出
- 配置导入导出

#### 🐚 交互式Shell
- 命令历史
- 自动补全
- Shell命令集成

#### 🧪 测试工具
- 完整测试套件
- 代码检查
- 自动修复
- 覆盖率报告

---

## 📦 安装

```bash
pip install ai-toolkit
```

### 前置要求
- Python 3.8+
- Ollama (用于本地模型)

---

## 💡 快速使用

### 1. 初始化
```bash
ai-toolkit init
```

### 2. 下载模型
```bash
ai-toolkit models pull llama3.2
```

### 3. AI编码助手
```bash
ai-toolkit coding generate "写一个快速排序"
```

### 4. Web UI
```bash
ai-toolkit webui
# 访问 http://localhost:8000
```

### 5. 交互式Shell
```bash
ai-toolkit shell
```

---

## 📚 完整功能

### 核心功能 (21个模块，75+命令)

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
| batch | 1 | 批处理 |
| schedule | 4 | 任务调度 |
| export | 3 | 数据导出 |
| monitor | 3 | 系统监控 |
| backup | 3 | 备份恢复 |
| system | 4 | 系统管理 |
| diag | 3 | 诊断工具 |
| shell | 1 | 交互式Shell |
| guide | 2 | 快速指南 |
| 其他 | 6 | 初始化、升级、状态 |

---

## 📊 技术栈

- Python 3.8+
- Click, Rich, Pydantic
- FastAPI, Uvicorn
- ChromaDB
- 10个API Key轮换

---

## 🔗 链接

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **文档**: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

## 🎯 路线图

### v0.4.0 (下个版本)
- [ ] Web UI增强
- [ ] 多LLM支持
- [ ] 性能优化

### v1.0.0 (目标)
- [ ] 完整Web UI
- [ ] 企业功能
- [ ] 云服务

---

## ⭐ 如果这个项目对你有帮助，请给个 Star！

**下载**: `pip install ai-toolkit`

**Star**: https://github.com/flowerjunjie/ai-toolkit

---

**🚀 让AI开发更简单！**
