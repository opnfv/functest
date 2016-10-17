#!/bin/bash -e

# Script checks that venv exists. If it doesn't it will be created
# It requires python2.7 and virtualenv packages installed
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

BASEDIR=`dirname $0`
VENV_PATH=$1
VENV_NAME="venv_cloudify"
function venv_install() {
    if command -v virtualenv-2.7; then
        virtualenv-2.7 $1
    elif command -v virtualenv2; then
        virtualenv2 $1
    elif command -v virtualenv; then
        virtualenv $1
    else
        echo Cannot find virtualenv command.
        return 1
    fi
}

# exit when something goes wrong during venv install
set -e
if [ ! -d "$VENV_PATH/$VENV_NAME" ]; then
    venv_install $VENV_PATH/$VENV_NAME
    echo "Virtualenv" + $VENV_NAME + "created."
fi

if [ ! -f "$VENV_PATH/$VENV_NAME/updated" -o $BASEDIR/requirements.pip -nt $VENV_PATH/$VENV_NAME/updated ]; then
    source $VENV_PATH/$VENV_NAME/bin/activate
    pip install -r $BASEDIR/requirements.pip
    touch $VENV_PATH/$VENV_NAME/updated
    echo "Requirements installed."
    deactivate
fi
set +e
