#!/bin/sh

VOL_DEV_NAME="$(lsblk |awk '/vdc/sdc {print $1}')"

if [[ ! -z $VOL_DEV_NAME ]]; then
    sudo mkdir -p ~/volume;
    sudo /usr/sbin/mkfs.ext4 -F /dev/$VOL_DEV_NAME;
    sudo mount /dev/$VOL_DEV_NAME ~/volume;
    if mount | grep volume; then
        sudo touch ~/volume/new_data
        echo "New data added to the volume!"
    else
        echo "Failed to write data!"
        exit 1
    fi
fi
