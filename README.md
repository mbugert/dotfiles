# dotfiles
To be installed on top of XFCE on Debian/Ubuntu.

* i3wm
    * primarily using the tabbed layout with title bar icons for common apps
    * i3lock-fancy-rapid
* polybar
* feh
* compton
* redshift
* exponential screen brightness (for greater control over low brightness region)

## General Hints
* http://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html

## Notable Tweaks

### Focus VSCodium before opening files
By default, if one has VSCodium/VSCode instances open on multiple i3 workspaces and opens a file through thunar, the last VSCodium instance which received focus will open the file, not an instance on the same workspace. This way, files tend to open off-screen for no good reason. [Video demonstration here](https://www.reddit.com/r/i3wm/comments/l28iol/how_to_always_use_vscodium_instance_from_current/).

This is fixed here by modifying [the VSCodium .desktop entry](.local/share/applications/codium.desktop) by wrapping it with [a script](mimeapps/.local/bin/focus_before_launch.sh) which tries to focus a VSCodium instance on the current workspace before opening a file.