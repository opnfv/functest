FROM opnfv/functest-core:kali

ARG BRANCH=stable/kali
ARG OPENSTACK_TAG=master
ARG VMTP_TAG=master
ARG NEUTRON_TAG=master

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /^tempest==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" pip3 install --no-cache-dir -cupper-constraints.txt -cupper-constraints.opnfv.txt lxml ;; esac && \
    git init /src/vmtp && \
    (cd /src/vmtp && \
        git fetch --tags https://review.opendev.org/x/vmtp.git $VMTP_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/vmtp/ && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest#egg=tempest/ upper-constraints.txt && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/vmtp && \
    mkdir -p /home/opnfv/functest/data/rally/neutron && \
    git init /src/neutron && \
    (cd /src/neutron && \
        git fetch --tags https://opendev.org/openstack/neutron.git $NEUTRON_TAG && \
        git checkout FETCH_HEAD) && \
    cp -r /src/neutron/rally-jobs /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/vmtp /src/neutron && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
