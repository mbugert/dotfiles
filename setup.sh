#!/usr/bin/env bash
set -o errexit

echo "[i] Ask for sudo password"
sudo -v

# Install ansible if necessary
if [ -f /etc/os-release ]
    then
        . /etc/os-release

        case "$ID" in
            debian | ubuntu)
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

# Run main playbook
echo "[i] Run Playbook"
ansible-playbook ansible/dotfiles.yaml --ask-become-pass

echo "[i] Done."