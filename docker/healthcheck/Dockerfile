FROM opnfv/functest-core:kali

ARG ODL_TAG=89b88a0a23561f0bda62338b394ec41655679b2d
ARG TEMPEST_HORIZON_TAG=1.0.0

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev openssl-dev && \
    git init /src/tempest-horizon && \
    (cd /src/tempest-horizon && \
        git fetch --tags https://opendev.org/openstack/tempest-horizon.git $TEMPEST_HORIZON_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/tempest-horizon/ && \
    pip3 install --use-deprecated=legacy-resolver --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        /src/tempest-horizon -rthirdparty-requirements.txt && \
    git init /src/odl_test && \
    (cd /src/odl_test && \
        git fetch --tags https://git.opendaylight.org/gerrit/integration/test $ODL_TAG && \
        git checkout FETCH_HEAD) && \
    rm -r /src/odl_test/.git /src/tempest-horizon/ thirdparty-requirements.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
