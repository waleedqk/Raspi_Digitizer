#!/bin/bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

MYHOME="/home/${SUDO_USER}"

# APP LIST
APP_LIST=(
    cron
    g++
    gcc
    git
    iperf
    netcat
    nmap
    npm
    ntp
    openssh-client
    openssh-server   
    packeth
    python-dev
    python3-dev
    python-pip
    python3-pip
    screen
    ssh
    sshfs
    tcpdump
    telnet
    tmux
    unzip
    vim
    wget
    wireshark
    xclip
    
)

# PIP3 LIST
PIP3_LIST=(
	pytube
)

APP3_LIST=(
    python-dev
    python3-dev
    python-pip
    python3-pip
	python3-nmap
)

config_dir()
{
    # Remove unused folders
    rm -rf $MYHOME/Templates
    rm -rf $MYHOME/Examples
    # sudo apt-get purge wolfram-engine -y
    mkdir -p $MYHOME/Documents/git
    mkdir -p $MYHOME/Downloads
    mkdir -p $MYHOME/Pictures
    mkdir -p $MYHOME/Videos
    mkdir -p $MYHOME/Music
}

apt_update()
{
    echo "update..."
    apt-get update
}

install_app()
{
    echo "Installing apps now ..."
    sudo apt-get -y install "${APP_LIST[@]}"
}


pip_update()
{

	echo "update pip..."
	sudo -H pip3 install --upgrade pip
	sudo -H pip2 install --upgrade pip
}

install_python_modules()
{
    pip_update

     echo "Installing python apps now ..."
	sudo apt-get -y install "${APP3_LIST[@]}"

	echo "Installing pip3 apps"	
	sudo -H pip3 install "${PIP3_LIST[@]}"

	echo "Upgrading modules ..."
	sudo pip3 install --upgrade "${PIP3_LIST[@]}"
}

vim_config()
{
    BUNDLE="$MYHOME/.vim/bundle"
    if [ ! -d "$BUNDLE/Vundle.vim" ]; then
        sudo -u ${SUDO_USER} mkdir -p "$BUNDLE"
        sudo -u ${SUDO_USER} git clone https://github.com/VundleVim/Vundle.vim.git "$BUNDLE/Vundle.vim"
    fi

    # Update existing (or new) installation
    cd "$BUNDLE/Vundle.vim"
    sudo -u ${SUDO_USER} git pull -q
    # In order to update Vundle.vim and all your plugins directly from the command line you can use a command like this:
    sudo -u ${SUDO_USER} vim -c VundleInstall -c quitall

    echo "Vim setup updated."

    if [ -f $MYHOME"/.vimrc" ] ; then
        rm $MYHOME"/.vimrc"
    fi
    sudo -u ${SUDO_USER} cp $REPO_DIR"/config/vim/vimrc" $MYHOME"/.vimrc"
}


tmux_config()
{

    if [ -f $MYHOME"/.tmux.conf" ] ; then
        rm $MYHOME"/.tmux.conf"
    fi
    sudo -u ${SUDO_USER} cp $REPO_DIR"/config/tmux/tmux.conf" $MYHOME"/.tmux.conf"
}

wireshark_config()
{
    echo "Give user privelages for wireshark"
    sudo dpkg-reconfigure wireshark-common
    echo "a wireshark group been created in /etc/gshadow. so add user to it"
    sudo gpasswd -a $SUDO_USER wireshark
}

main()
{
    echo "Initializing fresh install" 

    config_dir
    apt_update
    install_app
    install_python_modules
    vim_config
    tmux_config
    wireshark_config
}

main