#!/bin/bash
vdn="$1"
if echo "$(lsblk|tail -n1)" |grep  $vdn ; then
    sudo mkdir -p -m 777 ~/volume;
    sudo mount /dev/$vdn ~/volume;
    if [[ $(ls ~/volume|grep new_data) ]]; then
        echo "Found existing data!";
     else
        echo "No data on volume!";
        exit 1
        
    fi
else
    echo "Device not found!"
    exit 1
fi
