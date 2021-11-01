#!/usr/bin/env bash

ELEMENTARY_XFCE_VERSION="0.15.2"

cd /tmp
wget https://github.com/shimmerproject/elementary-xfce/archive/refs/tags/v$ELEMENTARY_XFCE_VERSION.tar.gz
tar -xzf v$ELEMENTARY_XFCE_VERSION.tar.gz && rm v$ELEMENTARY_XFCE_VERSION.tar.gz
cd elementary-xfce-$ELEMENTARY_XFCE_VERSION
./configure
make -j$(nproc)
make install
make icon-caches