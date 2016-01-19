#!/bin/sh

while true; do
 ping -c 1 $1 2>&1 >/dev/null
 RES=$?
 if [ "Z$RES" = "Z0" ] ; then
  echo 'vPing OK'
 break
 else
  echo 'vPing KO'
 fi
 sleep 1
done