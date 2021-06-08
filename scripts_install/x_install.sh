#!/usr/bin/env bash

sudo apt update

# basic stuff
sudo apt install arandr feh guake i3-wm redshift-gtk rofi yad

sudo apt install python3-pip
yes | sudo pip3 install autorandr

# applications
sudo apt install gimp firefox keepassx

# manually:
# https://github.com/yvbbrjdr/i3lock-fancy-rapid
# https://github.com/polybar/polybar
# https://github.com/VSCodium/vscodium
# https://github.com/yshui/picom
# https://github.com/martin-ueding/thinkpad-scripts/