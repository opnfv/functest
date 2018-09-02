FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/queens
ARG VMTP_TAG=99b261ccccc2f8a08ee2d8fca9f54ef9d69899d7

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/git.openstack.org\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    git clone https://git.openstack.org/openstack/vmtp.git /src/vmtp && \
    (cd /src/vmtp && git fetch origin --tags $VMTP_TAG && git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/vmtp/ && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt src/vmtp && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
