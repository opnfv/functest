#!/bin/bash

set -e

PIP_PATH=~/.pip
PIP_CONF=$PIP_PATH/pip.conf
EASY_INSTALL_CONF=~/.pydistutil.cfg

if [ "x$BASE_PIP_URL" = "x" ];then
    exit 0
fi

echo "config pip and easy_install"
HOSTNAME=`echo $BASE_PIP_URL | awk -F '[:/]' '{print $4}'`
if [ "x$HOSTNAME" = "x" ]; then
    echo "invalid BASE_PIP_URL: $BASE_PIP_URL"
    exit 1
fi

if [ ! -d $PIP_PATH ];then
    mkdir $PIP_PATH
fi

echo -e "[global]\ntrusted-host = $HOSTNAME\nindex-url = $BASE_PIP_URL\ntimeout = 6000" > $PIP_CONF
echo -e "[easy_install]\nindex-url = $BASE_PIP_URL\nfind-links = $BASE_PIP_URL" > $EASY_INSTALL_CONF

