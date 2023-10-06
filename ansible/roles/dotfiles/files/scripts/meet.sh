#!/usr/bin/env bash

BASE_PATH="${HOME}/Documents/Drive/Personal/Meetings"
EDITOR=codium


if [ "$1" == "-h" ] ; then
    echo "Usage: `basename $0` [-h] NAME"
    exit 0
fi

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters. There must be one parameter: the meeting name."
    exit 1
fi


iso_today="$(date -I)"
path="${BASE_PATH}/${iso_today} ${1}.md"

# fill with default header
if [ ! -f "$path" ]; then
    echo "# ${iso_today} ${1}
" > "$path"
fi

# xdg-open should just work™, but it didn't, so I hardcode the editor
# xdg-open "${path}"
codium "${path}"
