#!/usr/bin/env bash
# Enable aggressive powersaving.

# terminate optional processes and services
pkill cloud-drive-ui
pkill redshift-gtk

service tailscaled stop
service bluetooth stop
service docker stop
service containerd stop
service openvpn stop
service virtualbox stop
service cups stop

# set tunables (this sets cpufreq governor to ondemand)
powertop --quiet --auto-tune

# manually set cpufreq governor on CPU 0 to powersave
cpufreq-set --cpu 0 --governor powersave

# turn off all CPUs but CPU 0
for online in /sys/devices/system/cpu/cpu[!0]*/online; do
    echo 0 > $online
done

# restart i3 and polybar (it will load an alternative powersaving bar)
sudo --set-home --user=#1000 i3-msg reload
