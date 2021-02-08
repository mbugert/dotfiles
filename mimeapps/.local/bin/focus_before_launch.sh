#!/usr/bin/env bash

# Tries to focus a given desktop application on the current i3 workspace before launching that application.
#
# Usage example:
#   focus_before_launch.sh VSCodium "/usr/share/codium/codium --no-sandbox --unity-launch" my_file_01.txt my_file_02.txt ...
# Arguments:
#   $1: WM_CLASS of desktop application this script tries to focus first
#   $2: command for launching the desired desktop application
#   anything behind $2: original arguments for desktop application

wm_class=$1
app_cmd=$2
shift; shift

# this can succeed or not, we don't care, important is to try it
i3-msg [class="${wm_class}" workspace="__focused__"] focus

# run original command with original args
${app_cmd} "$@"