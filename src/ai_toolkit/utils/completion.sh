"""
Bash 自动补全脚本
"""

# Bash completion for ai-toolkit
_ai_toolkit_completion() {
    local cur prev commands subcommands

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    commands="models prompts rag benchmark status init upgrade plugin batch schedule webui"

    # 主命令补全
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
        return 0
    fi

    # 子命令补全
    command="${COMP_WORDS[1]}"

    case "${command}" in
        models)
            subcommands="list pull run delete info"
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "${subcommands}" -- ${cur}))
            fi
            ;;
        prompts)
            subcommands="list add run show edit delete"
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "${subcommands}" -- ${cur}))
            fi
            ;;
        rag)
            subcommands="create query list delete"
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "${subcommands}" -- ${cur}))
            fi
            ;;
        benchmark)
            subcommands="run compare"
            if [[ ${COMP_CWORD} -eq 2 ]]; then
                COMPREPLY=($(compgen -W "${subcommands}" -- ${cur}))
            fi
            ;;
    esac
}

complete -F _ai_toolkit_completion ai-toolkit
