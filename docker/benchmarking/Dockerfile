FROM opnfv/functest-core:xena

ARG VMTP_TAG=34a82c9f3598ec7f5d8de0a6d5139b92931db4cc
ARG NEUTRON_TAG=master

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" \
        pip3 install --use-deprecated=legacy-resolver --no-cache-dir -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt lxml ;; esac && \
    git init /src/vmtp && \
    (cd /src/vmtp && \
        git fetch --tags https://review.opendev.org/x/vmtp.git $VMTP_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/vmtp/ && \
    pip3 install --use-deprecated=legacy-resolver --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        /src/vmtp && \
    mkdir -p /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    git init /src/neutron && \
    (cd /src/neutron && \
        git fetch --tags https://opendev.org/openstack/neutron.git $NEUTRON_TAG && \
        git checkout FETCH_HEAD) && \
    cp /src/neutron/rally-jobs/task-neutron.yaml /home/opnfv/functest/data/rally/neutron/rally-jobs/ && \
    rm -r /src/vmtp /src/neutron && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.9/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
