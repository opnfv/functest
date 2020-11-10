FROM opnfv/functest-tempest:iruya

ARG BRANCH=stable/iruya
ARG OPENSTACK_TAG=stable/stein
ARG TEMPEST_TAG=21.0.0
ARG VMTP_TAG=dc79be8a3b566507e1907a70fc9eaf0f1d6c9e9c

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /#egg=tempest/d upper-constraints.txt && \
    sed -i -E /^ujson==+.*$/d upper-constraints.txt && \
    sed -i -E /^kubernetes==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=rally/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=xrally-kubernetes/d upper-constraints.opnfv.txt && \
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" pip3 install --no-cache-dir -cupper-constraints.txt -cupper-constraints.opnfv.txt lxml ;; esac && \
    git init /src/vmtp && \
    (cd /src/vmtp && \
        git fetch --tags https://opendev.org/x/vmtp.git $VMTP_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/vmtp/ && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/vmtp && \
    mkdir -p /home/opnfv/functest/data/rally/neutron && \
    git init /src/neutron && \
    (cd /src/neutron && \
        git fetch --tags https://opendev.org/openstack/neutron.git $OPENSTACK_TAG && \
        git checkout FETCH_HEAD) && \
    cp -r /src/neutron/rally-jobs /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/vmtp /src/neutron && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.6/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
