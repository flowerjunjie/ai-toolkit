# 🤖 AI Toolkit - 本地AI工具箱

> 一个强大的本地AI模型管理和工具集，让AI开发更简单。

[![License: MIT](https://img.shoelace.ai/assets/badges/mit.svg)](LICENSE)
[![GitHub stars](https://img.shoelace.ai/assets/badges/github-stars.svg)](https://github.com/stars)

## ✨ 特性

- 🎯 **模型管理** - 快速下载、切换、删除本地AI模型
- 📝 **Prompt模板** - 管理和复用你的AI提示词
- 🚀 **快速RAG** - 一键搭建本地知识库问答
- 🧪 **性能测试** - 测试和对比不同模型的表现
- 🛠️ **CLI工具** - 简洁的命令行界面

## 🚀 快速开始

### 安装

```bash
pip install ai-toolkit
```

### 基本使用

```bash
# 查看已安装的模型
ai-toolkit models list

# 下载一个模型
ai-toolkit models pull llama3.2

# 测试模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"

# 管理Prompt模板
ai-toolkit prompts list
ai-toolkit prompts add my-prompt "你是一个专业的{角色}..."
ai-toolkit prompts run my-prompt --role "Python开发者"

# 快速搭建RAG
ai-toolkit rag create ./my-docs
ai-toolkit rag query "什么是RAG？"

# 性能测试
ai-toolkit benchmark --model llama3.2 --prompts ./tests.json
```

## 📦 安装

### 使用 pip
```bash
pip install ai-toolkit
```

### 使用 Docker
```bash
docker-compose up -d
```

### 从源码安装
```bash
git clone https://github.com/yourusername/ai-toolkit.git
cd ai-toolkit
pip install -e .
```

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Ollama (用于运行本地模型)

安装 Ollama:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 初始化
```bash
ai-toolkit init
```

### 基本使用

#### 模型管理
```bash
# 列出已安装的模型
ai-toolkit models list

# 下载一个模型
ai-toolkit models pull llama3.2

# 运行模型
ai-toolkit models run llama3.2 "你好，介绍一下你自己"
```

#### Prompt 模板
```bash
# 列出所有模板
ai-toolkit prompts list

# 添加新模板
ai-toolkit prompts add python-expert "你是一个专业的{language}开发者。请回答：{question}"

# 使用模板
ai-toolkit prompts run python-expert --vars language=Python,question="如何优化代码？"
```

#### RAG 知识库
```bash
# 创建知识库
ai-toolkit rag create ./my-docs --name my-kb

# 查询知识库
ai-toolkit rag query my-kb "什么是RAG？"

# 列出所有知识库
ai-toolkit rag list
```

#### 性能测试
```bash
# 运行基准测试
ai-toolkit benchmark run --model llama3.2 --iterations 5

# 对比多个模型
ai-toolkit benchmark compare llama3.2 mistral --prompt "介绍一下机器学习"
```

## 📖 文档

- [完整文档](https://ai-toolkit.readthedocs.io)
- [API参考](https://ai-toolkit.readthedocs.io/api)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 🎯 路线图

- [x] 基础CLI框架
- [x] 模型管理功能
- [x] Prompt模板系统
- [x] 基础RAG实现
- [ ] Web UI界面
- [ ] 更多模型支持
- [ ] 分布式部署

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## ☕️ 赞助支持

如果 AI Toolkit 对你有帮助，欢迎请我喝杯咖啡！

[![微信](https://img.shields.io/badge/微信-赞助-green?style=flat-square&logo=wechat)](docs/images/wechat-pay.jpg)
[![支付宝](https://img.shields.io/badge/支付宝-赞助-blue?style=flat-square&logo=alipay)](docs/images/alipay.jpg)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub-Sponsor-EA4AAA?style=flat-square&logo=GitHub+Sponsors)](https://github.com/sponsors/flowerjunjie)

详情请查看：[赞助说明](SPONSORSHIP.md)

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star 支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=flowerjunjie/ai-toolkit&type=Date)](https://star-history.com/#flowerjunjie/ai-toolkit&Date)

---

Made with ❤️ by [David](https://github.com/flowerjunjie)
