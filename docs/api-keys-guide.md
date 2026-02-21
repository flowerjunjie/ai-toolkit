# AI Toolkit API Key 配置说明

## 🔑 支持的 LLM 提供商

AI Toolkit v0.3.0 现在支持多个 LLM 提供商，并自动轮换使用 API Key！

### 已配置的提供商

#### 1. BigModel (智谱AI)
- **模型**: glm-4.7, glm-5
- **地址**: https://open.bigmodel.cn/api/anthropic
- **Key 数量**: 5 个
- **状态**: ✅ 已配置

#### 2. MiniMax
- **模型**: MiniMax-M2.5
- **地址**: https://api.minimaxi.com/anthropic
- **Key 数量**: 2 个
- **状态**: ✅ 已配置

#### 3. Kimi (月之暗面)
- **模型**: kimi-for-coding
- **地址**: https://api.kimi.com/coding/
- **Key 数量**: 2 个
- **状态**: ✅ 已配置

#### 4. Doubao (豆包)
- **模型**: Doubao-Seed-2.0-Code
- **地址**: https://ark.cn-beijing.volces.com/api/coding
- **Key 数量**: 1 个
- **状态**: ✅ 已配置

**总计**: 10 个 API Key

---

## 🔄 轮换策略

### 自动轮换
- API Key 自动循环使用
- 请求失败时自动切换到下一个
- 错误次数 > 10 时标记为不可用
- 所有 Key 不可用时自动重置

### 智能选择
```python
# 指定提供商
client = LLMClient(provider="bigmodel")

# 自动选择（默认）
client = LLMClient()
```

---

## 📊 使用示例

### 1. AI 编码助手

```bash
# 生成代码（自动选择提供商）
ai-toolkit coding generate "用Python写一个快速排序"

# 指定提供商
ai-toolkit coding generate "写一个Flask API" -p bigmodel

# 保存到文件
ai-toolkit coding generate "写一个二分查找" -o binary_search.py

# 代码审查
ai-toolkit coding review my_script.py

# 代码解释
ai-toolkit coding explain my_script.py

# 查看状态
ai-toolkit coding status
```

### 2. 查看使用统计

```bash
ai-toolkit coding status
```

输出：
```
🔑 API Key 状态

┏━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ 提供商    ┃ 模型       ┃ 状态   ┃ 请求数 ┃ 错误数 ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ bigmodel  │ glm-4.7    │ ✅ 可用 │ 15     │ 0      │
│ bigmodel  │ glm-5      │ ✅ 可用 │ 8      │ 0      │
│ minimax   │ MiniMax... │ ✅ 可用 │ 3      │ 0      │
│ kimi      │ kimi-for.. │ ✅ 可用 │ 5      │ 0      │
│ doubao    │ Doubao-..  │ ✅ 可用 │ 2      │ 0      │
└──────────┴────────────┴────────┴────────┴────────┘

总计: 10 个 API Key
可用: 10 个
```

---

## 🔧 添加新的 API Key

编辑文件：`src/ai_toolkit/core/api_manager.py`

```python
{
    "api_key": "your-api-key-here",
    "base_url": "https://api.provider.com/v1",
    "model": "model-name",
    "provider": "provider-name",
},
```

---

## 💡 最佳实践

1. **负载均衡**: 让系统自动轮换，不要指定提供商
2. **错误处理**: 系统会自动处理 API Key 失效
3. **监控**: 定期运行 `ai-toolkit coding status` 查看状态
4. **备份**: 保留多个 API Key 作为备份

---

## 🔒 安全提示

- API Key 已硬编码在源代码中
- 生产环境建议使用环境变量
- 不要在公开仓库中提交 API Key

---

**使用愉快！** 🚀
