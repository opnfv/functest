FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG BROWBEAT_TAG=master

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev gcc g++ libffi-dev \
        openssl-dev py-pip && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e git+https://github.com/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git clone https://github.com/openstack/browbeat.git -b $BROWBEAT_TAG /src/browbeat && \
    (cd /src/browbeat && git checkout $BROWBEAT_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/browbeat/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        /src/browbeat && \
    rm -r upper-constraints.txt /src/browbeat/.git
    pip install --no-cache-dir virtualenv setuptools
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
