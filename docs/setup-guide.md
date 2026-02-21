# AI Toolkit 开发指南

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/flowerjunjie/ai-toolkit.git
cd ai-toolkit
```

### 2. 安装依赖
```bash
pip install -e ".[dev]"
```

### 3. 配置 API Key（可选）
```bash
# 方法1: 使用环境变量
export BIGMODEL_1="your-api-key"
export MINIMAX_1="your-api-key"

# 方法2: 创建配置文件
python3 -c "from ai_toolkit.core.api_manager import create_sample_config; create_sample_config()"
# 然后编辑 ~/.ai-toolkit/api_keys.json
```

### 4. 运行测试
```bash
pytest tests/ -v
```

### 5. 运行代码检查
```bash
# 格式化
black src/ tests/

# 类型检查
mypy src/

# Lint
flake8 src/
```

---

## 🧪 测试

### 运行所有测试
```bash
pytest tests/ -v
```

### 运行特定测试
```bash
pytest tests/test_api_manager.py -v
```

### 测试覆盖率
```bash
pytest tests/ --cov=src/ai_toolkit --cov-report=html
```

---

## 📝 代码规范

### Python 风格
- 遵循 PEP 8
- 使用 Black 格式化
- 添加类型注解
- 编写文档字符串

### 提交规范
```
类型(范围): 简短描述

详细描述
```

类型:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档
- `test`: 测试
- `refactor`: 重构
- `style`: 格式
- `chore`: 构建

---

## 🔧 开发工作流

1. 创建功能分支
```bash
git checkout -b feature/your-feature
```

2. 编写代码和测试
```bash
# 编写代码
vim src/ai_toolkit/your_module.py

# 编写测试
vim tests/test_your_module.py
```

3. 运行测试
```bash
pytest tests/ -v
```

4. 格式化代码
```bash
black src/ tests/
```

5. 提交代码
```bash
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

---

## 📚 项目结构

```
ai-toolkit/
├── src/ai_toolkit/        # 源代码
│   ├── commands/          # 命令模块
│   ├── core/              # 核心模块
│   └── utils/             # 工具函数
├── tests/                 # 测试代码
├── docs/                  # 文档
└── scripts/               # 脚本
```

---

## 🐛 调试

### 启用调试模式
```bash
ai-toolkit --debug command
```

### 查看日志
```bash
tail -f ~/.ai-toolkit/logs/ai-toolkit.log
```

---

## ❓ 常见问题

### Q: 测试失败怎么办？
A: 确保安装了所有依赖: `pip install -e ".[dev]"`

### Q: 如何添加新命令？
A: 在 `src/ai_toolkit/commands/` 创建新文件，然后在 `cli.py` 中注册

### Q: API Key 如何配置？
A: 参考上方"配置 API Key"部分

---

**Happy Coding!** 🎉
