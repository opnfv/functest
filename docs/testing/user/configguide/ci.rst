Integration in CI
=================
In CI we use the Docker image and execute the appropriate commands within the
container from Jenkins.

Docker creation in set-functest-env builder `[3]`_::

    envs="-e INSTALLER_TYPE=${INSTALLER_TYPE} -e INSTALLER_IP=${INSTALLER_IP} -e NODE_NAME=${NODE_NAME}"
    [...]
    docker pull opnfv/functest:$DOCKER_TAG >/dev/null
    cmd="sudo docker run -id ${envs} ${volumes} ${custom_params} ${TESTCASE_OPTIONS} opnfv/functest:${DOCKER_TAG} /bin/bash"
    echo "Functest: Running docker run command: ${cmd}"
    ${cmd} >${redirect}
    sleep 5
    container_id=$(docker ps | grep "opnfv/functest:${DOCKER_TAG}" | awk '{print $1}' | head -1)
    echo "Container ID=${container_id}"
    if [ -z ${container_id} ]; then
        echo "Cannot find opnfv/functest container ID ${container_id}. Please check if it is existing."
        docker ps -a
        exit 1
    fi
    echo "Starting the container: docker start ${container_id}"
    docker start ${container_id}
    sleep 5
    docker ps >${redirect}
    if [ $(docker ps | grep "opnfv/functest:${DOCKER_TAG}" | wc -l) == 0 ]; then
        echo "The container opnfv/functest with ID=${container_id} has not been properly started. Exiting..."
        exit 1
    fi

    cmd="python ${FUNCTEST_REPO_DIR}/functest/ci/prepare_env.py start"
    echo "Executing command inside the docker: ${cmd}"
    docker exec ${container_id} ${cmd}


Test execution in functest-all builder `[3]`_::

    branch=${GIT_BRANCH##*/}
    echo "Functest: run $FUNCTEST_SUITE_NAME on branch ${branch}"
    cmd="functest testcase run $FUNCTEST_SUITE_NAME"
    fi
    container_id=$(docker ps -a | grep opnfv/functest | awk '{print $1}' | head -1)
    docker exec $container_id $cmd
    ret_value=$?
    exit $ret_value

Docker clean in functest-cleanup builder `[3]`_ calling docker rm and docker rmi


.. _`[3]`: https://git.opnfv.org/releng/tree/jjb/functest/functest-daily-jobs.yml
