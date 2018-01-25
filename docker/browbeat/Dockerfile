FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG VIMS_TAG=stable

RUN apk --no-cache add --update python3-dev libffi libffi-dev openssl-dev g++ make linux-headers && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://raw.githubusercontent.com/openstack/browbeat/master/requirements.txt \
        > requirements.txt && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt -r requirements.txt && \
    rm -r upper-constraints.txt requirements.txt
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
