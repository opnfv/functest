#!/bin/sh -e

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

VOL_DEV_NAME="$(lsblk -list | tr ' ' '\012'| grep "\\(vdc\\|sdc\\)")"

if [ -n $VOL_DEV_NAME ]; then
    sudo mkdir -p ./volume
    sudo /usr/sbin/mkfs.ext4 -F /dev/$VOL_DEV_NAME
    sudo mount /dev/$VOL_DEV_NAME ./volume
    sudo touch ./volume/new_data
    echo "New data added to the volume!"
else
    echo "Failed to write data!"
    exit 1
fi
