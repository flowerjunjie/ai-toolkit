# Zsh completion for ai-toolkit
# 安装: source <(ai-toolkit --completion-zsh)

#compdef ai-toolkit

_ai_toolkit() {
    local -a commands subcommands

    commands=(
        'models:管理本地AI模型'
        'prompts:管理Prompt模板'
        'rag:RAG知识库管理'
        'benchmark:性能测试'
        'status:显示系统状态'
        'init:初始化配置'
        'upgrade:检查更新'
        'help:显示帮助'
    )

    case $words[2] in
        models)
            subcommands=(
                'list:列出已安装的模型'
                'pull:下载一个模型'
                'run:运行模型生成文本'
                'delete:删除一个模型'
                'info:显示模型详细信息'
            )
            _describe 'command' subcommands
            ;;
        prompts)
            subcommands=(
                'list:列出所有Prompt模板'
                'add:添加一个Prompt模板'
                'run:运行一个Prompt模板'
                'show:显示Prompt模板详情'
                'edit:编辑Prompt模板'
                'delete:删除Prompt模板'
            )
            _describe 'command' subcommands
            ;;
        rag)
            subcommands=(
                'create:创建RAG知识库'
                'query:查询RAG知识库'
                'list:列出所有知识库'
                'delete:删除知识库'
            )
            _describe 'command' subcommands
            ;;
        benchmark)
            subcommands=(
                'run:运行性能测试'
                'compare:对比多个模型'
            )
            _describe 'command' subcommands
            ;;
        *)
            _describe 'command' commands
            ;;
    esac
}

_ai-toolkit "$@"
