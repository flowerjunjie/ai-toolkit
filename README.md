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

## 📖 文档

- [完整文档](https://ai-toolkit.readthedocs.io)
- [API参考](https://ai-toolkit.readthedocs.io/api)
- [贡献指南](CONTRIBUTING.md)

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

## 🌟 Star History

如果这个项目对你有帮助，请给个Star支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ai-toolkit&type=Date)](https://star-history.com/#yourusername/ai-toolkit&Date)

---

Made with ❤️ by David and BOSS
