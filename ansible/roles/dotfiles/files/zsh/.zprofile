#------ pyenv initial setup ------
export PYENV_ROOT="$HOME/.local/bin/pyenv"
path+=("$PYENV_ROOT/bin")

#------ write PATH env var after all changes from above, and run scripts depending on it ------
export PATH
eval "$(pyenv init -)"