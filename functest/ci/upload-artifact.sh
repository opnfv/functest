#!/bin/bash
# SPDX-license-identifier: Apache-2.0
##############################################################################
# Copyright (c) 2016 Orange and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e
set -o pipefail

export PATH=$PATH:/usr/local/bin/

project=$PROJECT
workspace=$WORKSPACE
artifact_dir="$project/docs"
DIRECTORY="$workspace"/"$1"

# check that the API doc directory does exist before pushing it to artifact
if [ ! -d "$DIRECTORY" ]; then
    echo "Directory to be uploaded "$DIRECTORY" does not exist"
    exit 1
fi
set +e
gsutil&>/dev/null
if [ $? != 0 ]; then
    echo "Not possible to push results to artifact: gsutil not installed"
    exit 1
else
    gsutil ls gs://artifacts.opnfv.org/"$project"/ &>/dev/null
    if [ $? != 0 ]; then
        echo "Not possible to push results to artifact: gsutil not installed."
        exit 1
    else
        echo "Uploading document to artifact $artifact_dir"
        gsutil -m cp -r "$DIRECTORY"/* gs://artifacts.opnfv.org/"$artifact_dir"/ >/dev/null 2>&1
    fi
fi
