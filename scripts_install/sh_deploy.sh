#!/usr/bin/env bash

echo "Switching login shell to 'zsh'"
chsh -s $(which zsh)
if [[ $? == 0 ]]; then
    echo "Done (restart session after to apply)"
fi