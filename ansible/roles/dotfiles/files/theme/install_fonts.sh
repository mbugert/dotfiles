#!/usr/bin/env bash

cd /tmp

# overpass font: https://github.com/RedHatBrand/Overpass
wget https://github.com/RedHatOfficial/Overpass/releases/download/v3.0.5/overpass-3.0.5.zip
unzip -qq overpass-3.0.5.zip && rm overpass-3.0.5.zip
mkdir -p /usr/local/share/fonts/opentype
cp -r Overpass-3.0.5/desktop-fonts/overpass /usr/local/share/fonts/opentype
cp -r Overpass-3.0.5/desktop-fonts/overpass-mono /usr/local/share/fonts/opentype
rm -r Overpass-3.0.5

# fontawesome: https://fontawesome.com/how-to-use/on-the-desktop/setup/getting-started
wget https://use.fontawesome.com/releases/v5.15.0/fontawesome-free-5.15.0-desktop.zip
unzip -qq fontawesome-free-5.15.0-desktop.zip && rm fontawesome-free-5.15.0-desktop.zip
mkdir -p /usr/local/share/fonts/opentype/fontawesome
cp -r fontawesome-free-5.15.0-desktop/otfs/* /usr/local/share/fonts/opentype/fontawesome
rm -r fontawesome-free-5.15.0-desktop

fc-cache -f -v