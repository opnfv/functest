FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG VIMS_TAG=stable

RUN wget -q -O- https://github.com/openstack/browbeat/blob/master/requirements.txt > upper-constraints.txt && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt && \
    rm -r upper-constraints.txt
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
