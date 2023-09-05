import pathlib

# finding min_brightness requires trial & error, like this:
# `echo 30 > /sys/class/backlight/intel_backlight/brightness`
LVDS_SCREENS = [{"backlight_location": pathlib.Path("/sys/class/backlight/intel_backlight"),
                 "min_brightness": 28,
                 "min_nits": 1,
                 "max_nits": 300}]
