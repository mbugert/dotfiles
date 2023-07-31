#!/usr/bin/env bash
set -o errexit

echo "[i] Ask for sudo password"
sudo -v

# Install ansible if necessary
if [ -f /etc/os-release ]
    then
        . /etc/os-release

        case "$ID" in
            debian | ubuntu | linuxmint)
                if [[ ! -x /usr/bin/ansible ]]; then
                    echo "[i] Install Ansible"
                    sudo apt install --no-install-recommends -y ansible
                fi
                ;;

            arch | manjaro)
                if [[ ! -x /usr/bin/ansible ]]; then
                    echo "[i] Install Ansible"
                    sudo pacman -Syu ansible --noconfirm
                fi
                ;;

            *)
                echo "[!] Unsupported Linux Distribution: $ID"
                exit 1
                ;;
        esac
    else
        echo "[!] Unsupported Linux Distribution"
        exit 1
    fi

# Install ansible dependencies
echo "[i] Install Ansible Dependencies"
ansible-galaxy collection install -r requirements.yaml

# Export a short machine identifier, which can later be used to load
# device-specific i3, polybar, and other config settings.
echo "[i] Determine Machine Identifier"
if [ -f /var/lib/dbus/machine-id ]; then
    export MACHINE_ID=$(cat /var/lib/dbus/machine-id | sha256sum | cut -c -3)
else
    export MACHINE_ID=missingno
fi

# Run main playbook
echo "[i] Run Playbook"
cd ansible && ansible-playbook dotfiles.yaml --ask-become-pass

echo "[i] Done."