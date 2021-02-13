#!/usr/bin/env bash

# overpass font: https://github.com/RedHatBrand/Overpass
wget https://github.com/RedHatBrand/Overpass/releases/download/3.0.2/overpass-desktop-fonts.zip
unzip -qq overpass-desktop-fonts.zip
sudo mkdir -p /usr/share/fonts/opentype
sudo cp -r overpass /usr/share/fonts/opentype
sudo cp -r overpass-mono /usr/share/fonts/opentype
rm -r overpass overpass-mono

# fontawesome: https://fontawesome.com/how-to-use/on-the-desktop/setup/getting-started
wget https://use.fontawesome.com/releases/v5.12.0/fontawesome-free-5.12.0-desktop.zip
unzip -qq fontawesome-free-5.12.0-desktop.zip
sudo mkdir -p /usr/share/fonts/opentype/fontawesome
sudo cp -r fontawesome-free-5.12.0-desktop/otfs/* /usr/share/fonts/opentype/fontawesome
rm -r fontawesome-free-5.12.0-desktop

sudo fc-cache -f -v