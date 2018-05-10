#!/bin/sh

VOL_DEV_NAME="$(lsblk |awk '/vdc/sdc {print $1}')"

if [[ ! -z $VOL_DEV_NAME ]]; then
    sudo mount /dev/$VOL_DEV_NAME ~/volume;
    if echo ~/volume/*new_data*; then
        echo "Found existing data!";
    else
        echo "No data found on the volume!";
        exit 1
    fi
fi
