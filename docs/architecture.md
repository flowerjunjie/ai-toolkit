# AI Toolkit 架构文档

## 📐 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      CLI层                              │
│  (cli.py, commands/)                                    │
│  - 命令解析                                             │
│  - 用户交互                                             │
│  - 参数验证                                             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                     核心层                              │
│  (core/)                                                │
│  - 配置管理 (config.py)                                 │
│  - API管理 (api_manager.py)                            │
│  - LLM客户端 (llm_client.py)                            │
│  - 向量存储 (vector_store.py)                           │
│  - 文档加载 (document_loader.py)                         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                     工具层                              │
│  (utils/)                                               │
│  - 日志 (logger.py)                                     │
│  - 进度条 (progress.py)                                 │
│  - 错误处理 (errors.py)                                 │
│  - 缓存 (cache.py)                                      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    外部服务                              │
│  - Ollama (本地模型)                                     │
│  - BigModel/MiniMax/Kimi/Doubao (API)                    │
│  - ChromaDB (向量数据库)                                 │
└─────────────────────────────────────────────────────────┘
```

## 🔄 数据流

### 模型运行流程
```
用户输入 → CLI解析 → API管理器 → LLM客户端 → 外部API → 返回结果 → 显示
```

### RAG查询流程
```
用户输入 → CLI解析 → 向量存储 → 相似度搜索 → 排序 → 返回结果 → 显示
```

## 📦 模块说明

### CLI层 (cli.py, commands/)
- **cli.py**: 主入口，命令路由
- **commands/**: 各功能命令实现
  - models.py: 模型管理
  - prompts.py: Prompt模板
  - rag.py: RAG知识库
  - coding.py: AI编码助手
  - etc.

### 核心层 (core/)
- **config.py**: 配置管理（带缓存）
- **api_manager.py**: API Key轮换管理
- **llm_client.py**: LLM统一接口
- **vector_store.py**: 向量存储封装
- **document_loader.py**: 文档加载和分块
- **cache.py**: 缓存系统
- **http_client.py**: HTTP连接池

### 工具层 (utils/)
- **logger.py**: 日志系统
- **progress.py**: 进度条
- **errors.py**: 错误处理
- **helpers.py**: 辅助函数

## 🔐 安全设计

### API Key管理
- 支持环境变量
- 支持配置文件
- 自动轮换使用
- 错误自动切换

### 输入验证
- Pydantic模型验证
- 用户输入清理
- 路径遍历防护

## ⚡ 性能优化

### 缓存策略
- LRU缓存：配置文件
- 磁盘缓存：向量结果
- 连接池：HTTP请求

### 惰性加载
- 按需导入模块
- 延迟初始化对象
- 减少启动时间

## 🧪 测试架构

```
tests/
├── conftest.py          # 测试配置
├── test_api_manager.py  # API管理测试
├── test_vector_store.py # 向量存储测试
├── test_llm_client.py   # LLM客户端测试
└── test_utils.py        # 工具函数测试
```

## 📊 依赖关系

### 核心依赖
- Click: CLI框架
- Rich: 终端美化
- Pydantic: 数据验证
- Requests: HTTP客户端
- ChromaDB: 向量数据库

### 可选依赖
- sentence-transformers: 文本嵌入
- pytest: 测试框架
- black: 代码格式化

## 🚀 扩展性

### 添加新命令
1. 在 `commands/` 创建文件
2. 定义命令函数
3. 在 `cli.py` 注册

### 添加新LLM提供商
1. 在 `api_manager.py` 添加配置
2. 在 `llm_client.py` 适配接口

### 添加新功能
1. 核心逻辑放在 `core/`
2. 工具函数放在 `utils/`
3. CLI命令放在 `commands/`

---

**架构原则**:
- 模块化设计
- 单一职责
- 依赖注入
- 接口隔离
