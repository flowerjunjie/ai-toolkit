# 🎯 创建 GitHub Release v0.2.0 操作指南

## 步骤 1: 访问 GitHub Releases 页面

点击链接或手动访问：
```
https://github.com/flowerjunjie/ai-toolkit/releases/new
```

## 步骤 2: 填写 Release 信息

### 基本信息
- **Tag**: `v0.2.0` (点击 "Choose a tag" 会自动提示创建新标签)
- **Target**: `main` (选择 main 分支)
- **Title**: `🎉 AI Toolkit v0.2.0 - 交互式初始化和自动补全`

### Release 内容

复制下面的内容到描述框：

---

```markdown
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

### 启用自动补全

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
```

---

## 💡 主要功能

- 🤖 **模型管理**: list/pull/run/delete/info
- 📝 **Prompt 模板**: add/run/show/edit/delete
- 🚀 **RAG 知识库**: create/query/list/delete
- 🧪 **性能测试**: run/compare
- ⚙️ **系统管理**: status/init/upgrade

---

## 📊 技术栈

- **语言**: Python 3.8+
- **框架**: Click, Rich, Pydantic
- **平台**: Ollama API

---

## 🔗 链接

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **文档**: https://github.com/flowerjunjie/ai-toolkit/blob/main/README.md
- **赞助**: https://github.com/flowerjunjie/ai-toolkit/blob/main/SPONSORSHIP.md

---

## 🙏 致谢

感谢所有贡献者和用户的反馈！

---

## 📅 下一个版本 (v0.3.0)

- 🎯 真正的向量检索 RAG (ChromaDB)
- 🤖 多模型支持
- 🔌 插件系统
- 🌐 Web UI

**敬请期待！** 🚀
```

---

## 步骤 3: 发布设置

### 勾选选项
- ✅ **Set as the latest release** (设为最新版本)

### Assets（可选）
如果想上传构建包，可以上传：
- `dist/ai_toolkit-0.2.0.tar.gz`
- `dist/ai_toolkit-0.2.0-py3-none-any.whl`

## 步骤 4: 发布

点击 **"Publish release"** 按钮即可！

---

## ✅ 发布后检查清单

- [ ] Release 页面显示正确
- [ ] 标签 v0.2.0 已创建
- [ ] README 中的版本号正确
- [ ] 赞助链接可点击
- [ ] 文档链接正确

---

**准备就绪！去创建 Release 吧！** 🚀

直接访问：https://github.com/flowerjunjie/ai-toolkit/releases/new
