FROM opnfv/functest-core:jerma

ARG BRANCH=stable/jerma
ARG OPENSTACK_TAG=stable/train
ARG ODL_TAG=89b88a0a23561f0bda62338b394ec41655679b2d
ARG TEMPEST_HORIZON_TAG=0.2.0

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev openssl-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /^tempest==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /^tempest==+.*$/d upper-constraints.opnfv.txt && \
    git init /src/tempest-horizon && \
    (cd /src/tempest-horizon && \
        git fetch --tags https://opendev.org/openstack/tempest-horizon.git $TEMPEST_HORIZON_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/tempest-horizon/ && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/tempest-horizon -rthirdparty-requirements.txt && \
    git init /src/odl_test && \
    (cd /src/odl_test && \
        git fetch --tags https://git.opendaylight.org/gerrit/integration/test $ODL_TAG && \
        git checkout FETCH_HEAD) && \
    rm -r /src/odl_test/.git /src/tempest-horizon/ thirdparty-requirements.txt \
        upper-constraints.txt upper-constraints.opnfv.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
