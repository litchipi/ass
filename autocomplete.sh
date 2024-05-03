CMD="assistant"

SRC="$(realpath ${BASH_SOURCE[0]})"
SRC="$(dirname $SRC)"

function _assistant_complete() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local prev=${COMP_WORDS[COMP_CWORD-1]}

    args=$(IFS=" "; echo "${COMP_WORDS[*]}")
    res=$(python3 "$SRC/lib/cli.py" $args)
    COMPREPLY=( $(compgen -W "$res" -- $cur) )
    return 0
}

complete -F _assistant_complete "$CMD"
