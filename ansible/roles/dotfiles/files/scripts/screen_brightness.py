#!/usr/bin/env python3

# Copyright (c) 2022 mbugert. MIT-licensed.
#
# Screen brightness control with exponential scale. Inspired by
# https://konradstrack.ninja/blog/changing-screen-brightness-in-accordance-with-human-perception/
#
# * Supports laptop screens (via ACPI) and external screens (via DDC/CI,
#   needs `ddcutil``).
# * The luminance range of each screen can be specified to make sure the
#   effective luminance is homogenous across screens of different brands,
#   manufacturers, etc.


from dataclasses import dataclass, field
from math import log10
from pathlib import Path

import argparse
import sys
import subprocess


SCREENS = {
    "lvds": [
        # finding min_brightness requires trial & error, like this:
        # `echo 30 > /sys/class/backlight/intel_backlight/brightness`
        {"backlight_location": Path("/sys/class/backlight/intel_backlight"),
         "min_brightness": 30,
         "min_nits": 1,
         "max_nits": 300}
    ],
    "ddc": [
        {"bus_number": 8,
         #"model_name": "LA2205",
         "min_nits": 40,
         "max_nits": 85}
    ]
}


# Apart from using __post_init__, we don't mutate screen objects, so this
# qualifies as a "specialized use case" as mentioned in the python docs
# for using unsafe_hash.
@dataclass(unsafe_hash=True)
class LVDSScreen:
    backlight_location: Path
    min_nits: int
    max_nits: int
    min_brightness: int
    max_brightness: int = field(init=False)
    
    def __post_init__(self):
        # read max brightness value
        cmd = ["cat", self.backlight_location / "max_brightness"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
            self.max_brightness = int(result.stdout)
        except CalledProcessError:
            self.max_brightness = None

    def get_brightness(self) -> int:
        cmd = ["cat", self.backlight_location / "actual_brightness"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
            return int(result.stdout)
        except CalledProcessError:
            return None

    def set_brightness(self, brightness: int):
        with (self.backlight_location / "brightness").open("w") as f:
            subprocess.run(["echo", str(brightness)], stdout=f)


@dataclass(unsafe_hash=True)
class DDCScreen:
    # TODO switch to selection by model name, which didn't work for my setup
    bus_number: int
    min_nits: int
    max_nits: int
    min_brightness: int = 1
    max_brightness: int = 100

    def get_brightness(self) -> int:
        cmd = ["ddcutil",
               "--terse",
               f"--bus={str(self.bus_number)}",
               "getvcp",
               "10"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
            # "VCP 10 C 42 100", where 42 is the current value
            return int(result.stdout.split()[-2])
        except CalledProcessError:
            return None

    def set_brightness(self, brightness: int):
        cmd = ["ddcutil",
               "--noverify",
               f"--bus={str(self.bus_number)}",
               "setvcp",
               "10",
               str(brightness)]
        subprocess.run(cmd)


def change_brightness(args):
    num_steps = args.steps

    # collect screens and pick reference screen from which to take the current
    # brightness: first LVDS screen if one is available, otherwise the first
    # DDC screen
    screens = []
    ref = None
    if args.lvds:
        lvds_screens = [LVDSScreen(**kwargs) for kwargs in SCREENS.get("lvds", [])]
        ref = lvds_screens[0]
        screens += lvds_screens
    if args.ddc:
        ddc_screens = [DDCScreen(**kwargs) for kwargs in SCREENS.get("ddc", [])]
        if not args.lvds:
            ref = ddc_screens[0]
        screens += ddc_screens
    if ref is None:
        return

    # determine luminance range shared by all screens (infimum, supremum)
    lumi_supremum = min(s.max_nits for s in screens)
    lumi_infimum = max(s.min_nits for s in screens)

    # compute each screen's brightness setting that matches the maximum
    # luminance of the darkest screen, and vice-versa for minimum
    # luminance
    log_bright_ranges = {}
    for s in screens:
        lumi_range = s.max_nits - s.min_nits
        bright_range = s.max_brightness - s.min_brightness
        pcnt_supremum = (lumi_supremum - s.min_nits) / lumi_range
        bright_supremum = s.min_brightness + pcnt_supremum * bright_range
        pcnt_infimum = (lumi_infimum - s.min_nits) / lumi_range
        bright_infimum = s.min_brightness + pcnt_infimum * bright_range

        # switch to log domain
        log_bright_ranges[s] = log10(bright_infimum), log10(bright_supremum)

    # compute current brightness step from the reference screen
    ref_log_bright_min, ref_log_bright_max = log_bright_ranges[ref]
    step = round(num_steps * (log10(ref.get_brightness()) - ref_log_bright_min)
               / (ref_log_bright_max - ref_log_bright_min))

    if args.increase:
        new_step = min(num_steps, step + 1)
    elif args.decrease:
        new_step = max(0, step - 1)
    else:
        raise AssertionError

    # per screen, compute and set new brightness setting
    for s in screens:
        log_bright_min, log_bright_max = log_bright_ranges[s]
        log_bright_new = log_bright_min + new_step / num_steps * \
                             (log_bright_max - log_bright_min)
        bright_new = round(10 ** log_bright_new)
        bright_new_clamped = max(min(bright_new, s.max_brightness),
                                 s.min_brightness)
        s.set_brightness(bright_new_clamped)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Change screen brightness.
Specify screen properties in the script for maximum usefulness.""")
    parser.add_argument("-s",
                        "--steps",
                        type=int,
                        default=20,
                        help="Number of brightness steps (default: 20).")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-i",
                       "--increase",
                       action="store_const",
                       const=True,
                       help="Increase by one step.")
    action.add_argument("-d",
                       "--decrease",
                       action="store_const",
                       const=True,
                       help="Decrease by one step.")
    parser.add_argument("--lvds",
                        action="store_true",
                        help="Change brightness on LVDS screen(s).")
    parser.add_argument("--no-lvds",
                        dest="lvds",
                        action="store_false")
    parser.set_defaults(lvds=True)
    parser.add_argument("--ddc",
                        action="store_true",
                        help="Change brightness on external screen(s) via DDC/CI.")
    parser.add_argument("--no-ddc",
                        dest="ddc",
                        action="store_false")
    parser.set_defaults(ddc=False)

    args = parser.parse_args()

    if args.steps < 1:
        print("Number of brightness steps must be at least 2.")
        sys.exit(1)

    change_brightness(args)
