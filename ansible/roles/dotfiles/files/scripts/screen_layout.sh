#!/usr/bin/env bash
# Rofi picker for autorandr screen layouts.

# case-insensitive matching
ROFI_ARGS=(-theme Arc-Dark -p "Screen Layout" -i)

declare -A options
for profile in $(autorandr --detected); do
    # convert '45d_home_1x' -> 'home 1x'
    pretty_profile=$(echo "$profile" | sed -E 's/^[^_]*_//' | tr '_' ' ')
    options["🦄 ${pretty_profile}"]=$profile
done
options["🟰 common"]="common"
options["🦣 clone-largest"]="clone largest"
options["🚥 horizontal"]="horizontal"
options["🚦 vertical"]="vertical"

main() {
    # print the options separated by newline characters, sort them, then call rofi
    result=$(echo -e "$(printf "%s\n" "${!options[@]}" | sort)" | rofi -dmenu "${ROFI_ARGS[@]}")

    # rofi exit code == 0: normal operation
    # 10 <= exit code <= 28: keybindings used
    # anything else: canceled or something unforeseen happened
    if [[ $? == 0 || ($? -ge 10 && $? -le 28) ]]; then
        profile=${options[$result]}
        autorandr --load $profile

        # always need to reload the bars
        $HOME/.config/scripts/launch_polybar_feh.sh
    fi
}

main
