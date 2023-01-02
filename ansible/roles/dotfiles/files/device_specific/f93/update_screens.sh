#!/usr/bin/env sh

autorandr --change --default mobile_f93
$HOME/.config/scripts/launch_polybar.sh

# if the built-in monitor is used in the current configuration, ensure the touchscreen only maps to the built-in monitor
xrandr --listmonitors | grep LVDS1
if [ $? -eq 0 ]; then
    xinput --map-to-output $(xinput list --id-only "Wacom ISDv4 90 Pen stylus") LVDS1
    xinput --map-to-output $(xinput list --id-only "Wacom ISDv4 90 Pen eraser") LVDS1
fi