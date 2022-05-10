# Run Functest containers on Raspberry PI

All Functest containers (Hunter and newer) are cross-compiled for arm and arm64
via [travis-ci](https://travis-ci.org/collivier/functest/branches).
They are built on top of Alpine armhf to support most of Raspberry PI models.

All Docker manifests are published to run these containers via the same
commands whatever the architecture.

## Copy the image to the SD card

> https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
>
> This is very important, as you will lose all the data on the hard drive if you provide the wrong device name.
> Make sure the device name is the name of the whole SD card as described above, not just a partition. For example: sdd, not sdds1 or sddp1; mmcblk0, not mmcblk0p1.


## Install Docker

```shell
wget https://downloads.raspberrypi.org/raspbian/images/raspbian-2018-11-15/2018-11-13-raspbian-stretch.zip
unzip 2018-11-13-raspbian-stretch.zip
sudo dd bs=4M if=2018-11-13-raspbian-stretch.img of=/dev/mmcblk0 conv=fsync
```

## Install Docker

```shell
curl -sSL https://get.docker.com | sudo sh
```

## That's all folks
