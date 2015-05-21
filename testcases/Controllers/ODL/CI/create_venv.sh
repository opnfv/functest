#!/bin/bash -e

# Script checks that venv exists. If it doesn't it will be created
# It requires python2.7 and virtualenv packages installed

BASEDIR=`dirname $0`

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
if [ ! -d "$BASEDIR/venv" ]; then
    venv_install $BASEDIR/venv
    echo "Virtualenv created."
fi

if [ ! -f "$BASEDIR/venv/updated" -o $BASEDIR/requirements.pip -nt $BASEDIR/venv/updated ]; then
    source $BASEDIR/venv/bin/activate
    pip install -r $BASEDIR/requirements.pip
    touch $BASEDIR/venv/updated
    echo "Requirements installed."
    deactivate
fi
set +e
