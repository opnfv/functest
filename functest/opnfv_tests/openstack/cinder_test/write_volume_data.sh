#/bin/bash
get_blk=$(lsblk|grep vdc)
if [[ "${get_blk}" ]];
then
    echo -e "Volume found: \n ${get_blk}";
    sudo /usr/sbin/mkfs.ext4 -F /dev/vdc
    sudo mkdir -p -m 777 /mnt/volume
    sudo mount /dev/vdc /mnt/volume
    if [[ "$(mount|grep volume)" ]];
    then
      sudo touch  /mnt/volume/new_data && echo 'New data added to the volume'
    else
      echo 'No data on new volume'
    fi
else 
    echo 'Volume not atached!';
fi

