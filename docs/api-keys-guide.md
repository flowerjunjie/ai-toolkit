# AI Toolkit API Key 配置说明

## 🔑 支持的 LLM 提供商

AI Toolkit 支持多个 LLM 提供商，通过环境变量或配置文件管理 API Key。

### 支持的提供商

- BigModel (智谱AI)
- MiniMax
- Kimi (月之暗面)
- Doubao (豆包)

---

## 🔐 安全配置

### 方法1: 环境变量（推荐）

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
# BigModel
export BIGMODEL_1="your-api-key"
export BIGMODEL_2="your-api-key"

# MiniMax
export MINIMAX_1="your-api-key"
export MINIMAX_2="your-api-key"

# Kimi
export KIMI_1="your-api-key"
export KIMI_2="your-api-key"

# Doubao
export DOUBAO_1="your-api-key"
```

然后重新加载：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

### 方法2: 配置文件

创建配置文件 `~/.ai-toolkit/api_keys.json`：

```json
{
  "api_keys": [
    {
      "provider": "bigmodel",
      "model": "glm-4.7",
      "base_url": "https://open.bigmodel.cn/api/anthropic",
      "api_key": "your-api-key-here"
    },
    {
      "provider": "minimax",
      "model": "MiniMax-M2.5",
      "base_url": "https://api.minimaxi.com/immersion/anthropic",
      "api_key": "your-api-key-here"
    }
  ]
}
```

---

## 🔄 轮换策略

### 自动轮换
- API Key 自动循环使用
- 请求失败时自动切换
- 错误累积10次后标记不可用
- 全部不可用时自动重置

### 智能选择
```python
# 指定提供商
client = LLMClient(provider="bigmodel")

# 自动选择（默认）
client = LLMClient()
```

---

## 📝 使用示例

### 配置完成后

```bash
# 生成代码
ai-toolkit coding generate "写一个快速排序"

# 指定提供商
ai-toolkit coding generate "写一个Flask API" -p bigmodel

# 查看状态
ai-toolkit coding status
```

---

## ⚠️ 安全提示

- **不要将 API Key 提交到公开仓库**
- **使用环境变量存储敏感信息**
- **定期轮换 API Key**
- **监控使用量**

---

**配置完成后，开始使用 AI Toolkit！** 🚀
