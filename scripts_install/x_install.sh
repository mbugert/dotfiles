#!/usr/bin/env bash

sudo apt update

# basic stuff
sudo apt install arandr feh guake i3-wm redshift-gtk rofi yad

sudo apt install python3-pip
yes | sudo pip3 install autorandr

# applications
sudo apt install gimp firefox keepassx

# For setting display brightness via ACPI, one needs write permissions to /sys after every boot. One solution is udev, see https://wiki.archlinux.org/title/Backlight#Udev_rule
sudo sh -c 'echo "ACTION==\"add\", SUBSYSTEM==\"backlight\", KERNEL==\"intel_backlight\", GROUP=\"video\", MODE=\"0664\"" > /etc/udev/rules.d/60-backlight.rules'
sudo usermod -a -G video $USER

# manually:
# https://github.com/yvbbrjdr/i3lock-fancy-rapid
# https://github.com/polybar/polybar
# https://github.com/VSCodium/vscodium
# https://github.com/yshui/picom
# https://github.com/martin-ueding/thinkpad-scripts/