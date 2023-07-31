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


import argparse
import dataclasses
import math
import os
import pathlib
import subprocess
import sys

# device-dependent file
try:
    from lvds_screens import LVDS_SCREENS
except ImportError:
    LVDS_SCREENS = []


DDC_SCREENS = [
    {"model_name": "LG ULTRAFINE",
     "min_nits": 50,
     "max_nits": 400},
    {"model_name": "LA2205",
     "min_nits": 40,
     "max_nits": 85},
]

# Apart from using __post_init__, we don't mutate screen objects, so this
# qualifies as a "specialized use case" as mentioned in the python docs
# for using unsafe_hash.
@dataclasses.dataclass(unsafe_hash=True)
class LVDSScreen:
    backlight_location: pathlib.Path
    min_nits: int
    max_nits: int
    min_brightness: int
    max_brightness: int = dataclasses.field(init=False)
    
    def __post_init__(self):
        # read max brightness value
        cmd = ["cat", self.backlight_location / "max_brightness"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
            self.max_brightness = int(result.stdout)
        except subprocess.CalledProcessError:
            self.max_brightness = None

    def get_brightness(self) -> int:
        # Technically, "actual_brightness" would be the right value to check
        # here, however we had situations where actual_brightness < brightness,
        # in which case increasing just set "brightness" to a value it was
        # already at, deadlocking the whole script.
        cmd = ["cat", self.backlight_location / "brightness"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
        return int(result.stdout)

    def set_brightness(self, brightness: int) -> None:
        with (self.backlight_location / "brightness").open("w") as f:
            subprocess.run(["echo", str(brightness)], stdout=f)


@dataclasses.dataclass(unsafe_hash=True)
class DDCScreen:
    model_name: str
    min_nits: int
    max_nits: int
    min_brightness: int = 1
    max_brightness: int = 100

    def get_brightness(self) -> int:
        cmd = ["ddcutil",
               "--terse",
               "--model",
               self.model_name,
               "getvcp",
               "10"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True,
                                text=True)
        # "VCP 10 C 42 100", where 42 is the current value
        return int(result.stdout.strip().split()[-2])

    def set_brightness(self, brightness: int) -> None:
        cmd = ["ddcutil",
               "--noverify",
               "--model",
               self.model_name,
               "setvcp",
               "10",
               str(brightness)]
        subprocess.run(cmd)

    def is_available(self) -> bool:
        cmd = ["ddcutil",
               "--terse",
               "--model",
               self.model_name,
               "getvcp",
               "d6"]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True,
                                    text=True)
            # "VCP D6 SNC x01", where x01 means powered on
            is_powered_on = result.stdout.strip().split()[-1] == "x01"
            return is_powered_on
        except subprocess.CalledProcessError:
            return False


def change_brightness(args):
    num_steps = args.steps

    # collect screens and pick reference screen from which to take the current
    # brightness: first LVDS screen if one is available, otherwise the first
    # DDC screen
    screens = []
    ref = None
    if args.lvds:
        lvds_screens = [LVDSScreen(**kwargs) for kwargs in LVDS_SCREENS]
        if not lvds_screens:
            print("Cannot change LVDS screen brightness: no LVDS screens available.")
            sys.exit(1)
        ref = lvds_screens[0]
        screens += lvds_screens
    if args.ddc:
        ddc_screens = []
        for kwargs in DDC_SCREENS:
            screen = DDCScreen(**kwargs)
            # quite slow, but it works
            if screen.is_available():
                ddc_screens.append(screen)
        if not ddc_screens:
            print("Cannot change DDC screen brightness: no DDC screens available.")
            sys.exit(1)
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
        log_bright_ranges[s] = math.log10(bright_infimum), math.log10(bright_supremum)

    # compute current brightness step from the reference screen
    ref_log_bright_min, ref_log_bright_max = log_bright_ranges[ref]
    ref_brightness = ref.get_brightness()
    if ref_brightness is None:
        raise ValueError(f"Cannot determine brightness of {ref}.")
    step = round(num_steps * (math.log10(ref_brightness) - ref_log_bright_min)
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

        # Towards the lower brightness region, one step in log space can be
        # smaller than 1 brightness step when converted back to linear space.
        # Address this by always moving at least one brightness step.
        if args.increase:
            bright_new_corr = max(bright_new, s.get_brightness() + 1)
        elif args.decrease:
            bright_new_corr = min(bright_new, s.get_brightness() - 1)
        else:
            raise AssertionError

        bright_new_clamped = max(min(bright_new_corr, s.max_brightness),
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
