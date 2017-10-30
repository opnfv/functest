########################################
#   Docker container for FUNCTEST
########################################
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

# Environment variables
ARG BRANCH=master
ARG RALLY_TAG=stable/0.10
ARG OS_FAULTS_TAG=0.1.16
ARG ODL_TAG=e12ba90cd27577c4c6c70ee54f7d599b5f6777ba
ARG OPENSTACK_TAG=stable/ocata
ARG TEMPEST_TAG=17.0.0
ARG VIMS_TAG=stable
ARG REFSTACK_TAG=4e187b07672dd1c41cb7c94658f1c91edebf53a2
ARG REPOS_DIR=/home/opnfv/repos
ARG FUNCTEST_BASE_DIR=/home/opnfv/functest
ARG FUNCTEST_CONF_DIR=${FUNCTEST_BASE_DIR}/conf
ARG FUNCTEST_DATA_DIR=${FUNCTEST_BASE_DIR}/data
ARG FUNCTEST_IMAGES_DIR=${FUNCTEST_BASE_DIR}/images
ARG FUNCTEST_RESULTS_DIR=${FUNCTEST_BASE_DIR}/results
ARG FUNCTEST_DIR=/usr/local/lib/python2.7/dist-packages/functest/
ARG REPOS_VNFS_DIR=${REPOS_DIR}/vnfs

# Environment variables
ENV CONFIG_FUNCTEST_YAML ${FUNCTEST_DIR}/ci/config_functest.yaml
ENV REPOS_DIR ${REPOS_DIR}
ENV creds ${FUNCTEST_CONF_DIR}/openstack.creds

# Packaged dependencies
RUN apt-get update && apt-get install -y \
build-essential \
bundler \
crudini \
curl \
dnsmasq \
gcc \
git \
libffi-dev \
libgmp3-dev \
libpq-dev \
libssl-dev \
libxml2-dev \
libxslt-dev \
libzmq3-dev \
python-dev \
python-mock \
python-pip \
python3 \
python3-dev \
python3-pip \
postgresql \
ruby \
ruby-dev \
ruby-bundler \
ssh \
sshpass \
wget \
--no-install-recommends

RUN pip install --upgrade pip && easy_install -U setuptools==30.0.0
RUN python3 -m pip install --upgrade pip setuptools==30.0.0

RUN mkdir -p ${REPOS_VNFS_DIR} \
    && mkdir -p ${FUNCTEST_BASE_DIR}/results \
    && mkdir -p ${FUNCTEST_CONF_DIR} \
    && mkdir -p ${FUNCTEST_DATA_DIR} \
    && mkdir -p ${FUNCTEST_IMAGES_DIR} \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh

RUN git config --global http.sslVerify false

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest===.*$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ | \
        sed s/^requests===.*$/requests===2.13.0/ \
        > upper-constraints.txt && \
    pip install --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e git+https://github.com/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git clone --depth 1 https://github.com/openstack/os-faults.git -b $OS_FAULTS_TAG /src/os-faults && \
    update-requirements -s --source /src/openstack-requirements /src/os-faults/ && \
    git clone --depth 1 https://github.com/openstack/rally.git -b $RALLY_TAG /src/rally && \
    update-requirements -s --source /src/openstack-requirements /src/rally && \
    git clone https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd src/refstack-client && git checkout $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client && \
    pip install --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        /src/os-faults /src/rally -e/src/refstack-client && \
    pip install --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest \
        -rthirdparty-requirements.txt && \
    python3 -m pip install --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        doctor-tests && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally-manage db create && \
    rm thirdparty-requirements.txt upper-constraints.txt

# OPNFV repositories
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/fds /src/fds

# other repositories
RUN git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
        (cd src/odl_test && git checkout $ODL_TAG)
RUN git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test

# Install tempest venv and create symlink for running refstack-client
RUN ln -s /src/tempest /src/refstack-client/.tempest \
    && virtualenv --system-site-packages /src/tempest/.venv --python=python2

RUN cd /src/vims-test && bundle install

RUN sh -c 'curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -' \
    && sudo apt-get install -y nodejs \
    && cd /src/promise && sudo npm -g install npm@latest \
    && cd /src/promise/source && npm install

RUN echo ". ${FUNCTEST_DIR}/cli/functest-complete.sh" >> /root/.bashrc

CMD ["functest_restapi"]
