FROM opnfv/functest-tempest:hunter

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/rocky
ARG TEMPEST_TAG=21.0.0
ARG ODL_TAG=85448c9d97b89989488e675b29b38ac42d8674e4
ARG TEMPEST_HORIZON_TAG=0.1.0

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /#egg=tempest/d upper-constraints.txt && \
    sed -i -E /^kubernetes==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=rally/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=xrally-kubernetes/d upper-constraints.opnfv.txt && \
    git init /src/tempest-horizon && \
    (cd /src/tempest-horizon && \
        git fetch --tags https://opendev.org/openstack/tempest-horizon.git $TEMPEST_HORIZON_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/tempest-horizon/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/tempest-horizon/ -rthirdparty-requirements.txt && \
    git init /src/odl_test && \
    (cd /src/odl_test && \
        git fetch --tags https://git.opendaylight.org/gerrit/integration/test $ODL_TAG && \
        git checkout FETCH_HEAD) && \
    rm -r /src/odl_test/.git /src/tempest-horizon/ thirdparty-requirements.txt upper-constraints.txt \
        upper-constraints.opnfv.txt
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
