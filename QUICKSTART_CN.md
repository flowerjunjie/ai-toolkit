# AI Toolkit - 快速开始指南 🚀

## 5分钟快速上手

### 安装
```bash
pip install ai-toolkit
```

### 初始化
```bash
ai-toolkit init
```

### 第一个AI命令
```bash
# 拉取模型
ai-toolkit models pull llama2

# 运行推理
ai-toolkit models run llama2 "你好，世界！"
```

**恭喜！你已经成功运行了第一个AI命令！** 🎉

---

## 10分钟构建RAG应用

### 步骤1: 创建知识库
```bash
# 准备文档
mkdir my-docs
echo "AI Toolkit是一个强大的本地AI工具箱" > my-docs/intro.txt

# 创建知识库
ai-toolkit rag create my-knowledge my-docs

# 搜索
ai-toolkit rag search my-knowledge "什么是AI Toolkit？"
```

### 步骤2: 构建API
```bash
# 创建API网关
ai-toolkit gateway create --rag my-knowledge --port 8080

# 测试API
curl http://localhost:8080/query?q=如何使用？
```

**恭喜！你已经构建了一个RAG应用！** 🎉

---

## 15分钟AI编码助手

### 代码生成
```bash
# 生成Flask API
ai-toolkit coding generate "创建一个Flask API，有用户注册和登录"

# 代码审查
ai-toolkit coding review ./my-app

# 性能优化
ai-toolkit perf optimize ./my-app
```

### 代码测试
```bash
# 生成测试
ai-toolkit test generate ./my-app

# 运行测试
ai-toolkit test run ./my-app
```

**恭喜！你已经用AI加速了开发！** 🎉

---

## 30分钟企业级部署

### Docker部署
```bash
# 构建镜像
ai-toolkit docker build

# 运行容器
ai-toolkit docker run --env prod

# 查看日志
ai-toolkit logs tail
```

### 监控设置
```bash
# 启动监控
ai-toolkit monitor start

# 查看仪表板
ai-toolkit monitor dashboard
```

**恭喜！你已经部署了企业级应用！** 🎉

---

## 常见使用场景

### 场景1: 文档问答
```bash
# 1. 创建知识库
ai-toolkit rag create docs ./markdown

# 2. 启动Web UI
ai-toolkit webui --rag docs

# 3. 浏问 http://localhost:3000
```

### 场景2: 代码审查
```bash
# 审查整个项目
ai-toolkit coding review ./src

# 生成修复建议
ai-toolkit coding fix ./src

# 运行测试
ai-toolkit test run ./src
```

### 场景3: 性能测试
```bash
# 运行基准测试
ai-toolkit benchmark run --model llama2 --iterations 100

# 生成报告
ai-toolkit benchmark report
```

### 场景4: 团队协作
```bash
# 创建团队
ai-toolkit team create --name "AI Team"

# 邀请成员
ai-toolkit team invite dev@company.com

# 设置权限
ai-toolkit rbac grant --user alice --permission deploy
```

---

## 快速命令参考

### 模型管理
```bash
ai-toolkit models list                    # 列出模型
ai-toolkit models pull llama2              # 拉取模型
ai-toolkit models run llama2 "Hello"       # 运行推理
ai-toolkit models delete llama2            # 删除模型
```

### RAG
```bash
ai-toolkit rag create my-rag ./docs        # 创建知识库
ai-toolkit rag search my-rag "query"       # 搜索
ai-toolkit rag delete my-rag               # 删除
```

### 编码助手
```bash
ai-toolkit coding generate "prompt"        # 生成代码
ai-toolkit coding review ./src             # 审查代码
ai-toolkit coding fix ./src                # 修复代码
```

### 测试
```bash
ai-toolkit test generate ./src             # 生成测试
ai-toolkit test run ./src                  # 运行测试
ai-toolkit test cover ./src                # 覆盖率
```

### DevOps
```bash
ai-toolkit docker build                    # 构建镜像
ai-toolkit docker run                      # 运行容器
ai-toolkit monitor start                   # 启动监控
ai-toolkit logs tail                       # 查看日志
```

---

## 故障排除

### 问题1: 模型拉取失败
```bash
# 检查Ollama状态
ai-toolkit diag ollama

# 重启Ollama
ai-toolkit diag ollama-restart
```

### 问题2: RAG性能慢
```bash
# 优化索引
ai-toolkit rag optimize my-rag

# 使用更快的嵌入模型
ai-toolkit rag config my-rag --embedding fast
```

### 问题3: 内存不足
```bash
# 使用量化模型
ai-toolkit models pull llama2:q4

# 清理缓存
ai-toolkit cache clear
```

---

## 进阶技巧

### 技巧1: 批量处理
```bash
# 批量推理
ai-toolkit models batch llama2 queries.txt

# 批量嵌入
ai-toolkit rag batch-embed docs/*.txt
```

### 技巧2: 自定义命令
```bash
# 创建别名
ai-toolkit alias create "deploy" "docker run --env prod"

# 使用别名
ai-toolkit deploy
```

### 技巧3: 自动化工作流
```bash
# 创建工作流
ai-toolkit workflow create my-workflow

# 添加步骤
ai-toolkit workflow add-step my-workflow --name "test" --cmd "test run"

# 运行工作流
ai-toolkit workflow run my-workflow
```

---

## 获取帮助

### 内置帮助
```bash
ai-toolkit --help                    # 总帮助
ai-toolkit models --help             # 模块帮助
ai-toolkit models run --help         # 命令帮助
```

### 社区支持
- 📖 文档: https://docs.ai-toolkit.dev
- 💬 Discord: https://discord.gg/ai-toolkit
- 🐛 GitHub: https://github.com/flowerjunjie/ai-toolkit/issues

### 商业支持
- 📧 Pro: support@ai-toolkit.dev
- 📞 Enterprise: enterprise@ai-toolkit.dev

---

## 下一步

### 学习资源
- 📚 完整文档: https://docs.ai-toolkit.dev
- 🎥 视频教程: https://youtube.com/@ai-toolkit
- 📝 博客: https://blog.ai-toolkit.dev

### 升级到Pro
```bash
# 查看Pro功能
ai-toolkit commercial compare

# 升级到Pro
ai-toolkit subscription upgrade --to pro
```

### 企业咨询
```bash
# 联系销售
ai-toolkit sales contact

# 预约演示
ai-toolkit sales demo --schedule
```

---

**🚀 5分钟上手，15分钟开发，30分钟部署！**

**💡 AI Toolkit - 让AI开发更简单！**
