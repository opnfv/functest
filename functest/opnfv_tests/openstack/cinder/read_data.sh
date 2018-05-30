#!/bin/sh -e

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

DEST=$(pwd)/$(mktemp -d volumeXXX)
VOL_DEV_NAME="$(lsblk -l -o NAME | grep -o "vdc\|sdc\b")"
echo "VOL_DEV_NAME: $VOL_DEV_NAME"

if [ ! -z $VOL_DEV_NAME ]; then
    sudo mount /dev/$VOL_DEV_NAME $DEST
    if [ -f $DEST/new_data ]; then
        echo "Found new data!"
    else
        echo "Failed to find data!"
    exit 1
    fi
fi
