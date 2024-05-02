#!/usr/bin/env bash

# TODO  FIXME  IMPORTANT    Fixup autocompletion call on the lib

_get_autocomplete() {
  shift;
  COMPREPLY=$(assistant autocomplete -- "$@")
  return 0
}

complete -F _get_autocomplete assistant
