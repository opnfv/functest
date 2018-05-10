#!/bin/sh

if [[ ! -z $(echo "$(lsblk| awk '/vdc/ {print $1}')") ]]; then
    sudo mkdir -p -m 777 ~/volume;
    sudo /usr/sbin/mkfs.ext4 -F /dev/vdc;
    sudo mount /dev/vdc ~/volume;
else
    if [[ ! -z $(echo "$(lsblk| awk '/sdc/ {print $1}')") ]]; then
        sudo mkdir -p -m 777 ~/volume;
        sudo /usr/sbin/mkfs.ext4 -F /dev/sdc;
        sudo mount /dev/sdc ~/volume;
    fi
fi

if mount | grep volume; then
    sudo touch ~/volume/new_data
    echo "New data added to the volume!"
else
    echo "Failed to write data!"
    exit 1
fi
