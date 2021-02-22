#!/usr/bin/env bash

# what directories should be installable by all users including the root user
base=(
    # example
)

# folders that should, or only need to be installed for a local user
useronly=(
    alacritty
    aliases
    jsbeautifyrc
    zshrc
    tmux
    xmobar
    xmonad
    starship
)

# run the stow command for the passed in directory ($2) in location $1
stowit() {
    usr=$1
    app=$2
    # -v verbose
    # -t target
    stow -v -t ${usr} ${app}
}

echo ""
echo "Stowing apps for user: $(whoami)"

# install apps available to local users and root
for app in ${base[@]}; do
    stowit "${HOME}" $app
done

# install only user space folders
for app in ${useronly[@]}; do
    if [[ ! $USER = *"root"* ]]; then
        stowit "${HOME}" $app
    fi
done

echo ""
echo "##### ALL DONE"
