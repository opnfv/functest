FROM opnfv/functest-core:zed

ARG ODL_TAG=89b88a0a23561f0bda62338b394ec41655679b2d

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev openssl-dev && \
    git init /src/odl_test && \
    (cd /src/odl_test && \
        git fetch --tags https://git.opendaylight.org/gerrit/integration/test $ODL_TAG && \
        git checkout FETCH_HEAD) && \
    rm -r /src/odl_test/.git thirdparty-requirements.txt && \
    apk del .build-deps
COPY testcases.yaml /etc/xtesting/testcases.yaml
CMD ["run_tests", "-t", "all"]
