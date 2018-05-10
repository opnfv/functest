#!/bin/sh

sudo mkdir -p -m 777 ~/volume;

if [[ ! -z $(echo "$(lsblk| awk '/vdc/ {print $1}')") ]]; then
    sudo mount /dev/vdc ~/volume;
    else if [[ ! -z $(echo "$(lsblk| awk '/vdc/ {print $1}')") ]]; then
    sudo mount /dev/vdc ~/volume;
    fi
fi

if echo ~/volume/*new_data*; then
    echo "Found existing data!";
else
    exit "No data found on the volume!";
    exit 1
fi
