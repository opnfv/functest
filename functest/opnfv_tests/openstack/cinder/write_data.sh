#!/bin/sh -e

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

DEST=$(mktemp -d)
VOL_DEV_NAME=${1:-vdb}
echo "VOL_DEV_NAME: $VOL_DEV_NAME"

echo "$(lsblk -l -o NAME)"

if [ ! -z $(lsblk -l -o NAME | grep $VOL_DEV_NAME) ]; then
    sudo /usr/sbin/mkfs.ext4 -F /dev/$VOL_DEV_NAME
    sudo mount /dev/$VOL_DEV_NAME $DEST
    sudo touch $DEST/new_data
    if [ -f $DEST/new_data ]; then
        echo "New data added to the volume!"
        sudo umount $DEST
    fi
else
    echo "Failed to write data!"
    exit 1
fi

exit 0
