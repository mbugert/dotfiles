#!/usr/bin/env bash

# call me from root of dotfiles repository
stow --target=$HOME autorandr gtk-3 i3 mimeapps picom polybar redshift scripts vscodium xfce4
sudo stow --target=/ X11