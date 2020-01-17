sudo apt update

function install {
  which $1 &> /dev/null

  if [ $? -ne 0 ]; then
    echo "Installing: ${1}..."
    sudo apt install -y $1
  else
    echo "Already installed: ${1}"
  fi
}

# basic necessities to make this whole thing work
install stow
install redshift-gtk
install python3-pip
sudo pip3 install -y autorandr

# everyday utilities
install htop
install iftop
install git

# applications
install gimp
install firefox

