# AI Toolkit - FAQ 常见问题 ❓

## 基础问题

### Q1: AI Toolkit是什么？
**A:** AI Toolkit是一个强大的本地AI模型管理和开发工具，让AI开发更简单。它提供了60+功能模块，620+命令，覆盖AI开发的完整流程。

### Q2: AI Toolkit免费吗？
**A:** 是的！Community版完全免费，包含基础功能。Pro版($9.99/月)提供高级功能，Enterprise版($99.99/月)提供企业级支持。

### Q3: AI Toolkit和LangChain有什么区别？
**A:**
- **AI Toolkit**: 更简单（CLI工具）、更完整（60+模块）、更本地（隐私保护）
- **LangChain**: 更灵活（Python库）、需要编程、需要集成多个工具

**简单来说：AI Toolkit = LangChain + Ollama + 更多工具**

### Q4: 我需要什么硬件？
**A:**
- **最低配置**: 8GB RAM, CPU支持
- **推荐配置**: 16GB RAM, GPU（M1/M2或RTX 3060以上）
- **企业配置**: 32GB RAM, 专业GPU

### Q5: 支持哪些操作系统？
**A:** macOS, Linux, Windows (WSL2)

---

## 安装和配置

### Q6: 如何安装AI Toolkit？
**A:** 
```bash
pip install ai-toolkit
ai-toolkit init
```

### Q7: 如何配置Ollama？
**A:** AI Toolkit会自动检测Ollama。如果没有安装：
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# 验证安装
ai-toolkit diag ollama
```

### Q8: 如何更换模型存储位置？
**A:** 编辑配置文件 `~/.ai-toolkit/config.json`:
```json
{
  "models_dir": "/path/to/models"
}
```

### Q9: 如何设置API密钥？
**A:** 
```bash
# 方式1: 环境变量
export OPENAI_API_KEY="sk-..."

# 方式2: 配置文件
ai-toolkit config set openai.api_key "sk-..."
```

### Q10: 如何更新AI Toolkit？
**A:** 
```bash
pip install --upgrade ai-toolkit
```

---

## 功能使用

### Q11: 如何运行本地模型？
**A:** 
```bash
# 拉取模型
ai-toolkit models pull llama2

# 运行推理
ai-toolkit models run llama2 "你好"
```

### Q12: 如何构建RAG应用？
**A:** 
```bash
# 创建知识库
ai-toolkit rag create my-rag ./docs

# 搜索
ai-toolkit rag search my-rag "问题"

# 启动Web UI
ai-toolkit webui --rag my-rag
```

### Q13: 如何使用AI编码助手？
**A:** 
```bash
# 生成代码
ai-toolkit coding generate "创建Flask API"

# 审查代码
ai-toolkit coding review ./src

# 优化代码
ai-toolkit coding optimize ./src
```

### Q14: 如何部署应用？
**A:** 
```bash
# Docker部署
ai-toolkit docker build
ai-toolkit docker run

# Kubernetes部署
ai-toolkit k8s deploy
```

### Q15: 如何监控应用？
**A:** 
```bash
# 启动监控
ai-toolkit monitor start

# 查看仪表板
ai-toolkit monitor dashboard
```

---

## 性能和优化

### Q16: 如何提高推理速度？
**A:** 
```bash
# 使用量化模型
ai-toolkit models pull llama2:q4

# 使用GPU
ai-toolkit config set gpu.enabled true

# 优化缓存
ai-toolkit cache enable
```

### Q17: 如何减少内存使用？
**A:** 
```bash
# 使用INT4量化
ai-toolkit models pull llama2:q4

# 限制并发
ai-toolkit config set concurrency 2

# 清理缓存
ai-toolkit cache clear
```

### Q18: RAG搜索不准确怎么办？
**A:** 
```bash
# 优化分块
ai-toolkit rag config my-rag --chunk-size 500

# 使用重排序
ai-toolkit rag config my-rag --rerank true

# 混合检索
ai-toolkit rag config my-rag --hybrid true
```

### Q19: 如何提高并发性能？
**A:** 
```bash
# 增加worker
ai-toolkit config set workers 4

# 使用异步
ai-toolkit config set async true

# 负载均衡
ai-toolkit gateway scale --replicas 3
```

### Q20: 如何优化数据库性能？
**A:** 
```bash
# 使用FAISS
ai-toolkit rag config my-rag --vector-db faiss

# 索引优化
ai-toolkit rag optimize my-rag

# 缓存嵌入
ai-toolkit rag config my-rag --cache-embeddings true
```

---

## 故障排除

### Q21: Ollama连接失败？
**A:** 
```bash
# 检查Ollama状态
ai-toolkit diag ollama

# 重启Ollama
ai-toolkit diag ollama-restart

# 查看日志
ai-toolkit logs tail --service ollama
```

### Q22: 模型下载失败？
**A:** 
```bash
# 检查网络
ai-toolkit diag network

# 使用镜像
ai-toolkit config set registry.mirror https://mirror.ollama.com

# 重试下载
ai-toolkit models pull llama2 --retry 3
```

### Q23: 内存不足错误？
**A:** 
```bash
# 使用量化模型
ai-toolkit models pull llama2:q4

# 清理缓存
ai-toolkit cache clear

# 限制批处理
ai-toolkit config set batch-size 1
```

### Q24: 权限错误？
**A:** 
```bash
# 修复权限
sudo chown -R $USER ~/.ai-toolkit

# 使用sudo
sudo ai-toolkit models pull llama2
```

### Q25: 如何查看详细日志？
**A:** 
```bash
# 启用调试模式
ai-toolkit --verbose models run llama2 "test"

# 查看日志
ai-toolkit logs tail --level debug

# 导出日志
ai-toolkit logs export --file logs.txt
```

---

## 订阅和付费

### Q26: 如何升级到Pro版？
**A:** 
```bash
ai-toolkit subscription upgrade --to pro
```
然后访问支付链接完成订阅。

### Q27: 支持哪些支付方式？
**A:** 
- 信用卡（Visa, MasterCard, Amex）
- PayPal
- 加密货币（BTC, ETH, USDT）
- 支付宝/微信支付（国内）

### Q28: 如何取消订阅？
**A:** 
```bash
ai-toolkit subscription cancel
```
或访问账户设置取消。

### Q29: Pro版和Enterprise版有什么区别？
**A:** 
| 功能 | Community | Pro | Enterprise |
|------|-----------|-----|------------|
| 基础功能 | ✅ | ✅ | ✅ |
| 高级RAG | ❌ | ✅ | ✅ |
| 性能优化 | ❌ | ✅ | ✅ |
| 优先支持 | ❌ | ✅ | ✅ |
| 团队协作 | ❌ | ❌ | ✅ |
| SSO | ❌ | ❌ | ✅ |
| 审计日志 | ❌ | ❌ | ✅ |
| 专属支持 | ❌ | ❌ | ✅ |

### Q30: 如何申请退款？
**A:** 
```bash
ai-toolkit subscription refund --reason "原因"
```
30天内无条件退款。

---

## 企业功能

### Q31: 如何设置团队？
**A:** 
```bash
# 创建团队
ai-toolkit team create --name "MyTeam"

# 邀请成员
ai-toolkit team invite user@email.com

# 设置权限
ai-toolkit rbac grant --user alice --permission deploy
```

### Q32: 如何配置SSO？
**A:** 
```bash
# LDAP
ai-toolkit sso integrate --provider ldap

# OAuth
ai-toolkit sso integrate --provider oauth

# SAML
ai-toolkit sso integrate --provider saml
```

### Q33: 如何查看审计日志？
**A:** 
```bash
# 查看日志
ai-toolkit audit logs --last 7d

# 生成报告
ai-toolkit audit report --format pdf
```

### Q34: 如何设置监控告警？
**A:** 
```bash
# 配置Prometheus
ai-toolkit monitor setup --prometheus

# 设置告警
ai-toolkit monitor alert --name high-latency --threshold 1000ms
```

### Q35: 如何获取技术支持？
**A:** 
- **Community**: Discord社区
- **Pro**: support@ai-toolkit.dev
- **Enterprise**: 专属支持 + SLA保证

---

## 高级问题

### Q36: 如何开发插件？
**A:** 
```bash
# 创建插件
ai-toolkit plugin create my-plugin

# 安装插件
ai-toolkit plugin install ./my-plugin

# 开发文档: https://docs.ai-toolkit.dev/plugins
```

### Q37: 如何集成到CI/CD？
**A:** 
```bash
# 生成CI配置
ai-toolkit cicd generate --platform github

# 运行测试
ai-toolkit test run --ci
```

### Q38: 如何批量处理？
**A:** 
```bash
# 批量推理
ai-toolkit models batch llama2 queries.txt

# 批量嵌入
ai-toolkit rag batch-embed docs/*.txt
```

### Q39: 如何备份数据？
**A:** 
```bash
# 备份配置
ai-toolkit backup create --include models

# 恢复
ai-toolkit backup restore backup.tar.gz
```

### Q40: 如何迁移数据？
**A:** 
```bash
# 导出数据
ai-toolkit export --format json --output data.json

# 导入数据
ai-toolkit import --format json --input data.json
```

---

## 更多问题

### 还没找到答案？

**联系我们:**
- 📖 文档: https://docs.ai-toolkit.dev
- 💬 Discord: https://discord.gg/ai-toolkit
- 📧 邮件: support@ai-toolkit.dev
- 🐛 Issues: https://github.com/flowerjunjie/ai-toolkit/issues

**快速搜索:**
- 使用 `ai-toolkit --help` 查看命令帮助
- 使用 `ai-toolkit <command> --help` 查看具体命令

---

**❓ FAQ已完成！**

**💡 找不到答案？联系我们！**
