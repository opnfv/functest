#!/bin/bash

export REPOS_DIR=/home/opnfv/repos
export FUNCTEST_DIR=$REPOS_DIR/functest
export KINGBIRD_DIR=$REPOS_DIR/kingbird

declare -a FUNCTEST_REQUIREMENTS; \
FUNCTEST_REQUIREMENTS=( "python-openstackclient" \
                        "python-keystoneclient" \
                        "python-novaclient" \
                        "python-cinderclient" \
                        "python-neutronclient" \
                        "python-ceilometerclient" );

function requirements_alignment {
    local target_repo=$1

    for CLIENT_REQ in ${FUNCTEST_REQUIREMENTS[@]}
    do
        FUNCTEST_CLIENT_REQ=$(grep $CLIENT_REQ $FUNCTEST_DIR/requirements.txt)

        if [ "$FUNCTEST_CLIENT_REQ" == "" ]; then
            continue
        fi

        REQ_LN=$(awk "/${CLIENT_REQ}/"'{ print NR; exit }' ${target_repo}/requirements.txt)

        if [ "$REQ_LN" == "" ]; then
            continue
        fi

        sed "${REQ_LN}c ${FUNCTEST_CLIENT_REQ}" -i ${target_repo}/requirements.txt
    done
}

requirements_alignment $KINGBIRD_DIR
