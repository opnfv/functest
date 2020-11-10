FROM opnfv/functest-tempest:hunter

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/rocky
ARG TEMPEST_TAG=21.0.0
ARG VMTP_TAG=2.4.8

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
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
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" pip install --no-cache-dir -cupper-constraints.txt -cupper-constraints.opnfv.txt lxml ;; esac && \
    git init /src/vmtp && \
    (cd /src/vmtp && \
        git fetch --tags https://opendev.org/x/vmtp.git $VMTP_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/vmtp/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/vmtp && \
    mkdir -p /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    git init /src/neutron && \
    (cd /src/neutron && \
        git fetch --tags https://opendev.org/openstack/neutron.git $OPENSTACK_TAG && \
        git checkout FETCH_HEAD) && \
    sed "s/NeutronTrunks.create_and_list_trunk_subports/NeutronTrunks.create_and_list_trunks/g" \
        /src/neutron/rally-jobs/task-neutron.yaml > /home/opnfv/functest/data/rally/neutron/rally-jobs/task-neutron.yaml && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/vmtp /src/neutron && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
