#!/usr/bin/env bash

# Terminate already running polybar instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -x polybar >/dev/null; do sleep 1; done

# use status of cpu1 as a canary for whether we are powersaving
cpu1_online=$(cat /sys/devices/system/cpu/cpu1/online)

# Launch polybar on each monitor - https://github.com/polybar/polybar/issues/763#issuecomment-392960721
for m in $(polybar --list-monitors | cut -d":" -f1); do
    if [[ $cpu1_online == "1" ]]; then
        MONITOR=$m polybar --reload defaultbar &
    else
        MONITOR=$m polybar --reload lowpowerbar &
    fi
done

# Run feh with same random image on all screens, see https://www.reddit.com/r/i3wm/comments/6580vm/how_to_set_multiple_monitors_to_use_the_same/dg8fcqh/
WALL=$(find "${HOME}/Pictures/Wallpapers/" -type f | sort -R | tail -1)
feh --no-fehbg --bg-fill "$WALL"
