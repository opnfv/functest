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
ARG RALLY_TAG=0.8.1
ARG ODL_TAG=release/beryllium-sr4
ARG KINGBIRD_TAG=1.1.0
ARG VIMS_TAG=stable
ARG VROUTER_TAG=stable
ARG REPOS_DIR=/home/opnfv/repos
ARG FUNCTEST_BASE_DIR=/home/opnfv/functest
ARG FUNCTEST_CONF_DIR=${FUNCTEST_BASE_DIR}/conf
ARG FUNCTEST_DATA_DIR=${FUNCTEST_BASE_DIR}/data
ARG FUNCTEST_IMAGES_DIR=${FUNCTEST_BASE_DIR}/images
ARG FUNCTEST_RESULTS_DIR=${FUNCTEST_BASE_DIR}/results
ARG FUNCTEST_DIR=/usr/local/lib/python2.7/dist-packages/functest/
ARG REPOS_VNFS_DIR=${REPOS_DIR}/vnfs

# Environment variables
ENV HOME /home/opnfv
ENV CONFIG_FUNCTEST_YAML ${FUNCTEST_DIR}/ci/config_functest.yaml
ENV REPOS_DIR ${HOME}/repos
ENV creds ${FUNCTEST_CONF_DIR}/openstack.creds

WORKDIR ${HOME}

# Packaged dependencies
RUN apt-get update && apt-get install -y \
build-essential \
bundler \
crudini \
curl \
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
postgresql \
ruby1.9.1-dev \
ssh \
sshpass \
wget \
--no-install-recommends

RUN pip install --upgrade pip && easy_install -U setuptools==30.0.0

RUN mkdir -p ${REPOS_VNFS_DIR} \
    && mkdir -p ${FUNCTEST_BASE_DIR}/results \
    && mkdir -p ${FUNCTEST_CONF_DIR} \
    && mkdir -p ${FUNCTEST_DATA_DIR} \
    && mkdir -p ${FUNCTEST_IMAGES_DIR} \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh

RUN git config --global http.sslVerify false

COPY thirdparty-requirements.txt thirdparty-requirements.txt
COPY upper-constraints.txt upper-constraints.txt
RUN wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > o-upper-constraints.txt && \
    pip install --src /src -cupper-constraints.txt -co-upper-constraints.txt \
        git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest \
        -rthirdparty-requirements.txt && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally-manage db create && \
    rm thirdparty-requirements.txt upper-constraints.txt o-upper-constraints.txt

# OPNFV repositories
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/copper ${REPOS_DIR}/copper
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/domino ${REPOS_DIR}/domino
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/doctor ${REPOS_DIR}/doctor
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/promise ${REPOS_DIR}/promise
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/netready ${REPOS_DIR}/netready
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/fds ${REPOS_DIR}/fds

# other repositories
RUN git clone --depth 1 -b $ODL_TAG https://git.opendaylight.org/gerrit/p/integration/test.git ${REPOS_DIR}/odl_test
RUN git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test ${REPOS_VNFS_DIR}/vims-test
RUN git clone --depth 1 -b $VROUTER_TAG https://github.com/oolorg/opnfv-functest-vrouter.git ${REPOS_VNFS_DIR}/vrouter
RUN git clone --depth 1 https://github.com/wuwenbin2/OnosSystemTest.git ${REPOS_DIR}/onos

RUN add_images.sh

RUN gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
RUN curl -L https://get.rvm.io | bash -s stable

# SFC integration
RUN /bin/bash -c ". /usr/local/lib/python2.7/dist-packages/sfc/tests/functest/setup_scripts/tacker_client_install.sh"

# Install tempest venv and create symlink for running refstack-client
RUN ln -s /src/tempest /src/refstack-client/.tempest \
    && virtualenv --system-site-packages /src/tempest/.venv

RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd ${REPOS_VNFS_DIR}/vims-test \
    && rvm autolibs enable"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd ${REPOS_VNFS_DIR}/vims-test \
    && rvm install 1.9.3"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd ${REPOS_VNFS_DIR}/vims-test \
    && rvm use 1.9.3"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd ${REPOS_VNFS_DIR}/vims-test \
    && bundle install"

RUN sh -c 'curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -' \
    && sudo apt-get install -y nodejs \
    && cd ${REPOS_DIR}/promise && sudo npm -g install npm@latest \
    && cd ${REPOS_DIR}/promise/source && npm install

RUN echo ". ${FUNCTEST_DIR}/cli/functest-complete.sh" >> ${HOME}/.bashrc
