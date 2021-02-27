#!/usr/bin/env bash

# Call this script from the root of the dotfiles repository.

stow --target=$HOME autorandr gtk-3 i3 mimeapps picom polybar redshift scripts vscodium xfce4
sudo stow --target=/ X11

# changes to /etc/systemd are a bit ugly: we want to replace existing files but stow won't let us, so we have to move them out of the way manually first
sudo ./systemd/pre_stow.sh
sudo stow --target=/ --ignore=\.sh systemd

# enable locking of screen when sleeping
sudo systemctl enable i3-lock-fancy-rapid@$USER.service