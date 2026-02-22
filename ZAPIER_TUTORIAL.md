# 📖 Zapier设置教程 - BOSS专用

**您已经登录Zapier了，太棒了！**

---

## 🎯 目标

设置自动化：
- GitHub发布新版本 → 自动发Twitter
- GitHub发布新版本 → 自动发LinkedIn

---

## 📝 步骤1: 创建第一个Zap（GitHub → Twitter）

### 1.1 创建新Zap

1. **点击左上角** "+ Create Zap" 按钮
2. **选择触发器（Trigger）**

### 1.2 选择GitHub

1. **搜索**: 在搜索框输入 "GitHub"
2. **点击**: "GitHub" 图标
3. **选择事件**: 点击 "New Release" （新版本发布）
4. **点击**: "Continue" 按钮

### 1.3 连接GitHub账号

1. **点击**: "Sign in to GitHub"
2. **授权**: 输入GitHub账号密码（如果需要）
3. **点击**: "Authorize zapier" 授权
4. **等待**: "Continue" 按钮变绿

### 1.4 选择仓库

1. **Repository**: 选择 `flowerjunjie/ai-toolkit`
2. **点击**: "Test trigger" 测试触发器
3. **等待**: 显示最近的release
4. **点击**: "Continue" 继续

### 1.5 选择动作（Action）- Twitter

1. **搜索**: 输入 "Twitter"
2. **点击**: "Twitter" 图标
3. **选择事件**: "Create Tweet" （创建推文）
4. **点击**: "Continue" 按钮

### 1.6 连接Twitter账号

1. **点击**: "Connect Twitter account"
2. **授权**: 登录Twitter并授权Zapier
3. **点击**: "Authorize app" 授权
4. **等待**: "Continue" 按钮变绿

### 1.7 设置推文内容

**复制粘贴这个内容**：

```
🚀 刚发布：AI Toolkit v0.3.0

本地AI工具箱，790+命令，让AI开发更简单

✅ 76个功能模块
✅ 20+AI模型支持
✅ 企业级功能（SSO、多租户）
✅ GDPR/SOC2合规

GitHub: https://github.com/flowerjunjie/ai-toolkit

#AI #MachineLearning #OpenSource
```

**设置**：
1. **Tweet text**: 粘贴上面的内容
2. **点击**: "Test step" 测试
3. **检查**: 会发送一条测试推文
4. **点击**: "Continue" 继续

### 1.8 启动Zap

1. **检查**: 回顾整个Zap设置
2. **命名**: 输入名称 "GitHub Release → Twitter"
3. **点击**: "Publish Zap" 发布
4. **完成**: ✅ Zap已启动！

---

## 📝 步骤2: 创建第二个Zap（GitHub → LinkedIn）

### 2.1 创建新Zap

1. **点击左上角** "+ Create Zap" 按钮

### 2.2 设置触发器（同步骤1.2-1.4）

**完全一样**：
- GitHub → New Release
- 选择仓库: `flowerjunjie/ai-toolkit`
- 测试触发器

### 2.3 选择动作（Action）- LinkedIn

1. **搜索**: 输入 "LinkedIn"
2. **点击**: "LinkedIn" 图标
3. **选择事件**: "Create Share Post" （创建分享）
4. **点击**: "Continue" 按钮

### 2.4 连接LinkedIn账号

1. **点击**: "Connect LinkedIn account"
2. **授权**: 登录LinkedIn并授权
3. **点击**: "Allow" 授权
4. **等待**: "Continue" 按钮变绿

### 2.5 设置LinkedIn内容

**复制粘贴这个内容**：

**标题**:
```
AI Toolkit v0.3.0 - 企业级本地AI工具箱
```

**内容**:
```
很高兴宣布AI Toolkit v0.3.0正式发布！

AI Toolkit是一个强大的本地AI模型管理和开发工具，让AI开发更简单。

核心优势：
- 🎯 76个功能模块，790+命令
- 🔒 数据本地化，隐私保护
- 💰 节省97%API成本
- 🏢 企业级功能（SSO、多租户、GDPR/SOC2）

适用场景：
- 独立开发者：快速原型开发
- 初创公司：团队协作，权限管理
- 企业：本地部署，数据隐私，合规

定价：
- Community: 免费
- Pro: $9.99/月
- Enterprise: $999/月

GitHub: https://github.com/flowerjunjie/ai-toolkit

欢迎试用和反馈！
```

**设置**：
1. **Post visibility**: 选择 "Anyone" （公开）
2. **Post text**: 粘贴上面的内容
3. **点击**: "Test step" 测试
4. **检查**: 会发送一条测试LinkedIn
5. **点击**: "Continue" 继续

### 2.6 启动Zap

1. **检查**: 回顾整个Zap设置
2. **命名**: 输入名称 "GitHub Release → LinkedIn"
3. **点击**: "Publish Zap" 发布
4. **完成**: ✅ Zap已启动！

---

## 🎉 完成！自动化已设置！

### 已完成的Zap：

✅ **Zap 1**: GitHub Release → Twitter
- ✅ 仓库: flowerjunjie/ai-toolkit
- ✅ 触发: 新版本发布
- ✅ 动作: 自动发Twitter

✅ **Zap 2**: GitHub Release → LinkedIn
- ✅ 仓库: flowerjunjie/ai-toolkit
- ✅ 触发: 新版本发布
- ✅ 动作: 自动发LinkedIn

---

## 🧪 测试自动化

### 测试方法：

**选项A: 测试现有版本**

1. **回到Zapier**
2. **点击**: "GitHub Release → Twitter" Zap
3. **点击**: "Run" 按钮
4. **等待**: 自动触发
5. **检查**: Twitter上有新推文 ✅

**选项B: 创建测试版本**

1. **GitHub**: https://github.com/flowerjunjie/ai-toolkit/releases/new
2. **创建测试版本**:
   - Tag: `v0.3.1-test`
   - Title: `测试版本`
   - Description: `自动化测试`
3. **点击**: "Publish release"
4. **等待**: 1-2分钟
5. **检查**: Twitter和LinkedIn ✅

---

## 💡 日常使用

### 以后发布新版本：

**超级简单**：
1. **GitHub**: 发布新版本
2. **Zapier**: 自动检测
3. **Twitter/LinkedIn**: 自动发布 ✅

**完全自动化！**

---

## 🎯 总结

**您已经完成**：
- ✅ Zapier账号登录
- ✅ 连接GitHub
- ✅ 连接Twitter
- ✅ 连接LinkedIn
- ✅ 设置2个自动化Zap

**下次发布新版本时**：
- 自动发Twitter
- 自动发LinkedIn

---

**🎉 恭喜BOSS！自动化设置完成！**

**💰 搞到钱 → 更好的显卡 → 更强的模型！**
