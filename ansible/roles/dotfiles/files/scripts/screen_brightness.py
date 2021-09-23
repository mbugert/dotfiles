#!/usr/bin/env python3
# Source: https://konradstrack.ninja/blog/changing-screen-brightness-in-accordance-with-human-perception/
# With modifications to use ACPI instead of xbacklight.

from math import log10
from pathlib import Path

import sys
import subprocess


# needs trial & error to determine, like this:
# `echo 30 > /sys/class/backlight/intel_backlight/brightness`
min_brightness = 30

steps = 20
backlight_location = Path("/sys/class/backlight/intel_backlight")


def get_brightness():
    return int(subprocess.check_output(["cat",  backlight_location / "actual_brightness"]))


def get_max_brightness():
    return int(subprocess.check_output(["cat",  backlight_location / "max_brightness"]))


def set_brightness(backlight):
    with (backlight_location / "brightness").open("w") as f:
        subprocess.call(["echo", str(backlight)], stdout=f)


if __name__ == "__main__":

    if len(sys.argv) < 2 or sys.argv[1] not in ["-inc", "-dec"]:
        print("usage:\n\t{0} -inc / -dec".format(sys.argv[0]))
        sys.exit(0)
    action = sys.argv[1]

    curr_brightness = get_brightness()
    max_brightness = get_max_brightness()

    log_min_brightness = log10(min_brightness)
    log_max_brightness = log10(max_brightness)

    # get current step from current backlight brightness
    current_step = round(log10(curr_brightness) / (log_max_brightness - log_min_brightness) * steps)
    
    if action == "-inc":
        new_step = current_step + 1
    elif action == "-dec":
        new_step = current_step - 1

    # compute new backlight brightness from new step
    log_new_brightness = new_step / steps * (log_max_brightness - log_min_brightness)
    new_brightness = max(min(round(10 ** log_new_brightness), max_brightness), min_brightness)

    print("Current brightness: {0}\nChanging to: {1}".format(curr_brightness, new_brightness))
    set_brightness(new_brightness)