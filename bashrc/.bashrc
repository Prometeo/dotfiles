# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
    for rc in ~/.bashrc.d/*; do
        if [ -f "$rc" ]; then
            . "$rc"
        fi
    done
fi

#ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

# Rust configuration
unset rc
. "$HOME/.cargo/env"
export RUST_SRC_PATH="$(rustc --print sysroot)/lib/rustlib/src/rust/src"

# scm configuration
[ -s "/home/prometeo/.scm_breeze/scm_breeze.sh" ] && source "/home/prometeo/.scm_breeze/scm_breeze.sh"

# import aliases
source ~/.aliases

# Create a new directory and enter it
function mk() {
  mkdir -p "$@" && cd "$@"
}

# export to paths
export PATH="$HOME/.local/bin/:$PATH"

# Python
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
      eval "$(pyenv init --path)"
fi

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1

# starship
eval "$(starship init bash)"

# pyenv: list and activate one virtualenv
function pyv() {
    pyenv activate $(ls ~/.pyenv/versions | fzf --height 40% --reverse)
}

# search and execute command from history
fh() {
  eval $( (fc -l 1 || history) | fzf +s --tac | sed -E 's/ *[0-9]*\*? *//' | sed -E 's/\\/\\\\/g')
}

bind -f  ~/.inputrc
