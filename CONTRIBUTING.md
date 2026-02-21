# 贡献指南

感谢你对 AI Toolkit 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议，请：

1. 检查是否已有类似 issue
2. 创建新 issue，详细描述问题或建议
3. 提供复现步骤（如果是 bug）

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/yourusername/ai-toolkit.git
   cd ai-toolkit
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **开发**
   - 遵循现有代码风格
   - 添加必要的测试
   - 更新文档

4. **提交**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 代码规范

- 遵循 PEP 8
- 使用类型提示
- 添加 docstring
- 保持函数简洁

## 提交信息规范

使用 Conventional Commits：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## 开发环境

```bash
# 克隆项目
git clone https://github.com/yourusername/ai-toolkit.git
cd ai-toolkit

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖（开发模式）
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
flake8 src/
```

## 功能建议

我们特别欢迎以下方向：

- 新的模型支持
- 性能优化
- UI 改进
- 文档和教程
- 测试用例

## 许可证

提交代码即表示你同意将代码以 MIT 许可证发布。
