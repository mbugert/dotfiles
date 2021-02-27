#!/usr/bin/env bash

# if logind.conf/sleep.conf are symlinks already, move them out of the way
if [[ ! -h "/etc/systemd/logind.conf" ]]; then
    mv /etc/systemd/logind.conf /etc/systemd/logind.conf.dist
fi
if [[ ! -h "/etc/systemd/sleep.conf" ]]; then
    mv /etc/systemd/sleep.conf /etc/systemd/sleep.conf.dist
fi