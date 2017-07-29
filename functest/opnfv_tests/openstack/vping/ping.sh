#!/bin/sh


ping -c 1 $1 2>&1 >/dev/null
RES=$?
if [ "Z$RES" = "Z0" ] ; then
    echo 'vPing OK'
else
    echo 'vPing KO'
fi
