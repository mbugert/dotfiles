#!/usr/bin/env bash

sudo apt update

# basic necessities to make this whole thing work
sudo apt install stow htop iftop git ncdu zsh

# clone zsh plugins
readonly ZSH_DIR=~/.config/zsh/

if [[ ! -d "${ZSH_DIR}/powerlevel10k" ]]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_DIR}/powerlevel10k"
else
    echo "Cloned powerlevel10k repository already exists at ${ZSH_DIR}, skipping..."
fi

if [[ ! -d "${ZSH_DIR}/zsh-autosuggestions" ]]; then
    git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions "${ZSH_DIR}/zsh-autosuggestions"
else
    echo "Cloned zsh-autosuggestions repository already exists at ${ZSH_DIR}, skipping..."
fi