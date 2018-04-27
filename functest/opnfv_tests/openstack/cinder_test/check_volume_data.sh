#/bin/bash
get_blk=$(lsblk|grep vdc)
if [[ ${get_blk} ]]; then
    echo -e "Volume found: \n ${get_blk}";
    sudo mkdir -p /mnt/volume
    sudo mount /dev/vdc /mnt/volume
    if $(ls|grep new_data); then
      echo 'Found existing data on volume';
    else
      echo 'Volume not found!';
      exit 1;
    fi
fi 
