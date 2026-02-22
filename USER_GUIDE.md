# AI Toolkit - 使用指南

> 🚀 本地AI工具箱 - 1615+命令，122个功能模块

## 📋 目录

- [快速开始](#快速开始)
- [核心命令](#核心命令)
- [模块分类](#模块分类)
- [常用场景](#常用场景)
- [配置选项](#配置选项)
- [故障排除](#故障排除)

---

## 🚀 快速开始

### 安装

```bash
# 安装AI Toolkit
pip install ai-toolkit

# 或从源码安装
git clone https://github.com/flowerjunjie/ai-toolkit.git
cd ai-toolkit
pip install -e .
```

### 基础使用

```bash
# 查看所有模块
ai-toolkit super:all

# 搜索命令
ai-toolkit super:search "诊断"

# 快速启动
ai-toolkit super:quick chat

# 查看统计
ai-toolkit super:stats
```

---

## 🎯 核心命令

### AI聊天

```bash
# 与AI助手对话
ai-toolkit ai:chat --prompt "解释量子计算"

# 使用特定模型
ai-toolkit ai:chat --model gpt-4 --prompt "写一首诗"
```

### 医疗诊断

```bash
# 症状分析
ai-toolkit medical:symptom --symptom "头痛,发热"

# AI诊断
ai-toolkit medical:diagnose --symptoms "咳嗽,发热"
```

### 区块链

```bash
# 创建钱包
ai-toolkit blockchain:wallet --network ethereum

# 发送交易
ai-toolkit blockchain:transaction --amount 1.5
```

### 电商

```bash
# 创建店铺
ai-toolkit ecommerce:store --name "MyShop" --platform shopify

# 添加产品
ai-toolkit ecommerce:product --name "AI Tool" --price 99.99
```

---

## 📚 模块分类

### AI核心 (6个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| ai_core | 15 | AI基础功能 |
| ai_advanced | 15 | 高级AI功能 |
| nlp_core | 15 | 自然语言处理 |
| cv_core | 15 | 计算机视觉 |
| ml_core | 15 | 机器学习 |
| llm_core | 15 | 大语言模型 |

### 数据处理 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| data_processing | 15 | 数据处理 |
| database | 15 | 数据库操作 |
| etl | 15 | ETL流程 |
| data_quality | 15 | 数据质量 |
| streaming | 15 | 流式处理 |

### 开发工具 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| dev_tools | 15 | 开发工具 |
| git_tools | 15 | Git工具 |
| docker_tools | 15 | Docker工具 |
| k8s_tools | 15 | Kubernetes工具 |
| testing | 15 | 测试工具 |

### 云服务 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| aws | 15 | AWS云服务 |
| azure | 15 | Azure云服务 |
| gcp | 15 | GCP云服务 |
| aliyun | 15 | 阿里云 |
| tencent_cloud | 15 | 腾讯云 |

### DevSecOps (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| security_advanced | 15 | 高级安全 |
| devsecops | 15 | DevSecOps |
| monitoring_advanced | 15 | 高级监控 |
| logging_advanced | 15 | 高级日志 |

### 自动化 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| automation_advanced | 15 | 高级自动化 |
| workflow | 15 | 工作流 |
| scheduler | 15 | 调度器 |
| orchestration | 15 | 编排 |

### 通信 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| messaging | 15 | 消息传递 |
| notification | 15 | 通知 |
| voice | 15 | 语音 |
| video | 15 | 视频 |

### 科学计算 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| scientific | 15 | 科学计算 |
| bioinfo | 15 | 生物信息 |
| earth_science | 15 | 地球科学 |
| quantum | 15 | 量子计算 |
| space_science | 15 | 空间科学 |

### 金融科技 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| financial | 15 | 金融服务 |
| trading | 15 | 交易系统 |
| risk_management | 15 | 风险管理 |
| crypto | 15 | 加密货币 |
| insurtech | 15 | 保险科技 |

### 医疗健康 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| medical | 15 | 医疗诊断 |
| health_monitoring | 15 | 健康监控 |
| mental_health | 15 | 心理健康 |
| telemedicine | 15 | 远程医疗 |

### 生活服务 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| travel | 15 | 旅行规划 |
| lifestyle | 15 | 生活方式 |
| pet_care | 15 | 宠物护理 |
| senior_care | 15 | 老人护理 |
| personal_assistant | 15 | 个人助理 |

### 教育 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| education | 15 | 教育工具 |
| edtech | 15 | 教育科技 |
| training | 15 | 培训系统 |
| tutoring | 15 | 辅导系统 |

### 媒体 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| media_production | 15 | 媒体制作 |
| journalism | 15 | 新闻报道 |
| publishing | 15 | 出版发行 |
| content_creation | 15 | 内容创作 |

### 创意 (5个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| creative_tools | 15 | 创意工具 |
| design | 15 | 设计工具 |
| photography | 15 | 摄影 |
| writing | 20 | 写作工具 |
| art | 15 | 艺术创作 |

### 娱乐 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| gaming | 15 | 游戏开发 |
| virtual_worlds | 15 | 虚拟世界 |
| social_entertainment | 15 | 社交娱乐 |
| live_streaming | 15 | 直播系统 |

### 体育 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| fitness | 15 | 健身 |
| sports_analytics | 15 | 体育分析 |
| coaching | 15 | 教练系统 |
| sports_science | 15 | 体育科学 |

### 旅行 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| navigation | 15 | 导航系统 |
| local_discovery | 15 | 本地发现 |
| adventure | 15 | 冒险活动 |
| cultural_tourism | 15 | 文化旅游 |

### 区块链 & IoT (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| blockchain | 15 | 区块链 |
| iot | 15 | 物联网 |
| cybersecurity | 15 | 网络安全 |
| datascience | 15 | 数据科学 |

### 云 & 移动 & 游戏 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| cloud_native | 15 | 云原生 |
| mobile | 15 | 移动开发 |
| game_dev | 15 | 游戏开发 |
| qa_automation | 15 | QA自动化 |

### 法律 & 电商 & 教育 (4个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| legal_tech | 15 | 法律科技 |
| ecommerce | 15 | 电子商务 |
| edtech | 15 | 教育科技 |
| project_advanced | 8 | 项目管理 |

### 超级系统 (1个模块)

| 模块 | 命令数 | 描述 |
|------|--------|------|
| super | 15 | 超级系统 |

---

## 💡 常用场景

### 场景1: 数据科学项目

```bash
# 1. 数据清洗
ai-toolkit data_processing:clean --file data.csv

# 2. 数据探索
ai-toolkit datascience:explore --dataset data.csv

# 3. 机器学习
ai-toolkit datascience:ml --task classification

# 4. 模型部署
ai-toolkit datascience:deploy --model model.pkl
```

### 场景2: 区块链DApp开发

```bash
# 1. 创建钱包
ai-toolkit blockchain:wallet --network ethereum

# 2. 部署合约
ai-toolkit blockchain:smart --type erc20

# 3. 创建NFT
ai-toolkit blockchain:nft --name "MyNFT"

# 4. 构建DApp
ai-toolkit blockchain:dapp --type defi
```

### 场景3: 电商运营

```bash
# 1. 创建店铺
ai-toolkit ecommerce:store --name "MyShop"

# 2. 添加产品
ai-toolkit ecommerce:product --name "Product" --price 99.99

# 3. 数字营销
ai-toolkit ecommerce:marketing --channel email

# 4. 数据分析
ai-toolkit ecommerce:analytics --type sales
```

### 场景4: 在线教育

```bash
# 1. 创建课程
ai-toolkit edtech:course --subject "Python"

# 2. 创建测验
ai-toolkit edtech:quiz --type multiple

# 3. 自动批改
ai-toolkit edtech:grade --type auto

# 4. 生成证书
ai-toolkit edtech:certificate --type completion
```

---

## ⚙️ 配置选项

### 全局配置

```bash
# 查看配置
ai-toolkit super:config

# 设置配置
ai-toolkit super:config --key model --value gpt-4

# 设置温度
ai-toolkit super:config --key temperature --value 0.7
```

### 环境变量

```bash
# 设置API密钥
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."

# 设置模型
export AI_TOOLKIT_MODEL="gpt-4"
export AI_TOOLKIT_TEMPERATURE="0.7"
```

### 配置文件

```yaml
# ~/.ai-toolkit/config.yaml
model: gpt-4
temperature: 0.7
max_tokens: 2000
log_level: INFO
plugins:
  - openai
  - anthropic
  - huggingface
```

---

## 🔧 故障排除

### 常见问题

**Q: 命令找不到?**

```bash
# 检查安装
pip show ai-toolkit

# 重新安装
pip install --upgrade ai-toolkit
```

**Q: API密钥错误?**

```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 设置API密钥
export OPENAI_API_KEY="your-key"
```

**Q: 模块加载失败?**

```bash
# 检查依赖
pip check

# 安装依赖
pip install -r requirements.txt
```

**Q: 权限错误?**

```bash
# 使用sudo
sudo ai-toolkit <command>

# 或添加用户到docker组
sudo usermod -aG docker $USER
```

### 获取帮助

```bash
# 查看帮助
ai-toolkit --help

# 查看模块帮助
ai-toolkit <module> --help

# 查看命令帮助
ai-toolkit <module>:<command> --help

# 超级帮助
ai-toolkit super:help
```

### 健康检查

```bash
# 系统健康检查
ai-toolkit super:health

# 查看日志
ai-toolkit super:log --lines 100

# 查看统计
ai-toolkit super:stats
```

---

## 📞 获取支持

- **GitHub**: https://github.com/flowerjunjie/ai-toolkit
- **文档**: https://docs.ai-toolkit.com
- **社区**: https://discord.gg/ai-toolkit
- **邮件**: support@ai-toolkit.com

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

**产品为王** 💰 - **永远beta，持续迭代中！**
