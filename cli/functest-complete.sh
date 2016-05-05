_functest_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _FUNCTEST_COMPLETE=complete $1 ) )
    return 0
}

complete -F _functest_completion -o default functest;
