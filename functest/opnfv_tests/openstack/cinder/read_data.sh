#!/bin/sh -e

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

VOL_DEV_NAME="$(lsblk -l | grep -Po '^[vs]dc\W')"

if [ -n "$VOL_DEV_NAME" ]; then
    sudo mount /dev/$VOL_DEV_NAME /home/cirros/volume;
    if [ -f /home/cirros/volume/new_data ]; then
        echo "Found existing data!";
    else
        echo "No data found on the volume!";
        exit 1
    fi
fi
