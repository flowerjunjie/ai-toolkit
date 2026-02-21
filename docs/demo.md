# 🎬 AI Toolkit 演示脚本

## Terminal 演示 (录制视频/截图用)

### 场景1: 首次使用
```bash
# 安装
pip install ai-toolkit

# 初始化
ai-toolkit init

# 查看状态
ai-toolkit status
```

### 场景2: 模型管理
```bash
# 列出模型 (初始为空)
ai-toolkit models list

# 下载一个模型
ai-toolkit models pull llama3.2

# 再次列出
ai-toolkit models list

# 运行模型
ai-toolkit models run llama3.2 "用Python写一个快速排序"

# 查看模型信息
ai-toolkit models info llama3.2
```

### 场景3: Prompt 模板
```bash
# 添加模板
ai-toolkit prompts add code-review "你是一个专业的{language}代码审查员。请审查以下代码：\n\n{code}"

# 列出模板
ai-toolkit prompts list

# 查看模板详情
ai-toolkit prompts show code-review

# 使用模板
ai-toolkit prompts run code-review --vars language=Python,code="print('hello world')"
```

### 场景4: RAG 知识库
```bash
# 创建知识库
mkdir -p ~/my-docs
echo "AI Toolkit 是一个强大的本地AI工具箱" > ~/my-docs/intro.txt
ai-toolkit rag create ~/my-docs --name my-kb

# 查询知识库
ai-toolkit rag query my-kb "什么是AI Toolkit？"

# 列出知识库
ai-toolkit rag list
```

### 场景5: 性能测试
```bash
# 运行基准测试
ai-toolkit benchmark run --model llama3.2 --iterations 3

# 对比模型
ai-toolkit benchmark compare llama3.2 mistral --prompt "解释什么是量子计算"
```

## GIF 录制脚本

### 使用 asciinema (终端录制)
```bash
# 安装
pip install asciinema

# 录制
asciinema rec ai-toolkit-demo.cast

# 执行演示命令
# ... (上面的演示脚本)

# 结束录制: Ctrl+D

# 上传到 asciinema.org
asciinema upload ai-toolkit-demo.cast
```

### 使用 ttyrec (简化版)
```bash
# 安装
sudo apt-get install ttyrec

# 录制
ttyrec demo.tty

# 播放
ttyplay demo.tty

# 转换为 GIF (需要 ttyrec2gif)
ttyrec2gif demo.tty demo.gif
```

## 截图关键点

1. **主帮助页面** - `ai-toolkit --help`
2. **模型列表** - `ai-toolkit models list`
3. **运行模型** - `ai-toolkit models run llama3.2 "你好"`
4. **Prompt 模板列表** - `ai-toolkit prompts list`
5. **RAG 查询结果** - `ai-toolkit rag query my-kb "问题"`
6. **性能测试结果** - `ai-toolkit benchmark run`

## 视频演示大纲 (2-3分钟)

1. **介绍** (15秒)
   - 什么是 AI Toolkit
   - 为什么需要它

2. **安装和初始化** (20秒)
   - pip install
   - ai-toolkit init

3. **核心功能演示** (90秒)
   - 模型管理 (30秒)
   - Prompt 模板 (20秒)
   - RAG 知识库 (20秒)
   - 性能测试 (20秒)

4. **总结和号召** (15秒)
   - GitHub 地址
   - Star 和贡献

---

**提示**: 演示时使用真实数据，让用户看到实际效果！
