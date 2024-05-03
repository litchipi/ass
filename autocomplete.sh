CMD="assistant"

function _assistant_complete() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local prev=${COMP_WORDS[COMP_CWORD-1]}

    args=$(IFS=" "; echo "${COMP_WORDS[*]}")
    res=$(python3 ./lib/cli.py $args)
    COMPREPLY=( $(compgen -W "$res" -- $cur) )
    return 0
}

complete -F _assistant_complete "$CMD"
