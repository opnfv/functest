#!/bin/sh -e

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

VOL_DEV_NAME="$(lsblk -l -o NAME | grep -o "vdc\|sdc\b")"
echo "VOL_DEV_NAME: $VOL_DEV_NAME"

if [ ! -z $VOL_DEV_NAME ]; then
    sudo mkdir -p ./volume
    sudo /usr/sbin/mkfs.ext4 -F /dev/$VOL_DEV_NAME
    sudo mount /dev/$VOL_DEV_NAME ./volume/
    sudo touch ./volume/new_data
    if [ -f ./volume/new_data ]; then
        echo "New data added to the volume!"
        sudo umount ./volume/
    fi
else
    echo "Failed to write data!"
    exit 1
fi
