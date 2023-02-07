import pathlib

LVDS_SCREENS = [{"backlight_location": pathlib.Path("/sys/class/backlight/amdgpu_bl0"),
                 "min_brightness": 1,
                 "min_nits": 1,
                 "max_nits": 500}]
