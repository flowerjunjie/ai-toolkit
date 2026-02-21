# 🎉 AI Toolkit v0.3.0 发布说明

## 📢 重大更新

AI Toolkit v0.3.0 是一个**完整的、生产就绪的**本地AI工具箱！

### ✨ 新功能

#### 🎯 插件系统
- ✅ 动态插件加载
- ✅ 生命周期钩子
- ✅ 命令拦截
- ✅ 插件模板生成
- ✅ 热加载/卸载

#### 📦 批处理模式
- ✅ 从文件执行命令列表
- ✅ 并行执行支持
- ✅ 错误处理
- ✅ 进度显示
- ✅ 执行统计

#### ⏰ 任务调度
- ✅ 定时任务管理
- ✅ 多种时间单位
- ✅ 后台运行
- ✅ 任务列表

#### 🌐 Web UI
- ✅ FastAPI Web服务
- ✅ RESTful API
- ✅ 系统状态监控
- ✅ 代码生成接口
- ✅ API文档自动生成

### 🔧 性能优化
- ✅ LRU缓存系统
- ✅ 磁盘缓存
- ✅ HTTP连接池
- ✅ 配置文件缓存
- ✅ 惰性加载

### 🛡️ 安全增强
- ✅ API Key 环境变量支持
- ✅ 配置文件加载
- ✅ 输入验证
- ✅ 错误处理

### 🧪 测试和文档
- ✅ 测试框架搭建
- ✅ 单元测试覆盖
- ✅ 架构文档
- ✅ 开发指南
- ✅ API文档

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

### Web UI
```bash
ai-toolkit webui
# 访问 http://localhost:8000
```

---

## 💡 主要功能

### 核心功能 (11个)
1. ✅ 模型管理 (models)
2. ✅ Prompt模板 (prompts)
3. ✅ RAG知识库 (rag/rag2)
4. ✅ 性能测试 (benchmark)
5. ✅ AI编码助手 (coding)
6. ✅ 命令别名 (alias)
7. ✅ 历史记录 (history)
8. ✅ 配置管理 (config)
9. ✅ Web UI (webui)
10. ✅ 插件系统 (plugin)
11. ✅ 批处理 (batch)
12. ✅ 任务调度 (schedule)

### 总命令数：**50+**

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click, Rich, Pydantic, FastAPI
- **数据库**: ChromaDB
- **LLM**: 4个提供商 (BigModel/MiniMax/Kimi/Doubao)
- **Web**: FastAPI + Uvicorn
- **测试**: pytest

---

## 🔗 链接

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **文档**: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- **架构**: https://github.com/flowerjunjie/ai-toolkit/blob/main/docs/architecture.md
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

## 📦 完整变更

### 新增
- 插件系统 (plugin命令)
- 批处理模式 (batch命令)
- 任务调度 (schedule命令)
- Web API (webui命令)
- 缓存系统 (cache.py)
- HTTP连接池 (http_client.py)
- 性能优化
- 测试框架

### 优化
- API Key管理重构
- 配置缓存
- 错误处理统一
- 代码质量提升
- 文档完善

### 修复
- 移除API Key硬编码
- 修复类型注解
- 修复导入问题

---

## 🎯 里程碑

- [x] v0.1.0 - MVP (基础功能)
- [x] v0.2.0 - 用户体验 (交互式、补全)
- [x] v0.3.0 - 生产工具 (完整功能)

---

**下一个版本**: v0.4.0 (规划中)

**下载**: `pip install --upgrade ai-toolkit`

**⭐️ 如果这个项目对你有帮助，请给个 Star！**
