#!/bin/bash
vdn="$1"
if echo "$(lsblk|tail -n1)" |grep  $vdn ; then
    echo "New volume found";              
    sudo /usr/sbin/mkfs.ext4 -F /dev/$vdn;
    sudo mkdir -p -m 777 ~/volume;
    sudo mount /dev/$vdn ~/volume;
    if mount | grep $vdn; then       
        sudo touch ~/volume/new_data;        
        echo "New data added to the volume!";
    else
        echo "NO data added to the volume!"
        exit 1 
    fi
else                                    
    echo "NO volume device found!";
    exit 1 
fi



