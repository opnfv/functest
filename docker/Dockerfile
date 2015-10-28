########################################
#   Docker container for FUNCTEST
########################################
# Purpose: run all the tests against the POD
#          from a pre-installed docker image
#
# Maintained by Jose Lausuch
# Build:
#    $ docker build -t opnfv/functest:tag .
#
# Execution:
#    $ docker run -t -i \
#      -e "INSTALLER_TYPE=fuel/foreman" \
#      -e "INSTALLER_IP=10.20.0.2/172.30.10.73" \
#      -v $(pwd)/config_functest.yaml:/home/opnfv/functest/conf/config_functest.yaml
#      opnfv/functest /bin/bash
#
# NOTE: providing config_functest.yaml is optional. If not provided, it will
#       use the default one located in the repo


FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

ENV repos_dir /home/opnfv/repos

# Packaged dependencies
RUN apt-get update && apt-get install -y \
ssh \
sshpass \
curl \
git \
gcc \
wget \
python-dev \
python-pip \
bundler \
postgresql \
build-essential \
libpq-dev \
libxslt-dev \
libssl-dev \
libgmp3-dev \
libxml2-dev \
libffi-dev \
crudini \
--no-install-recommends


RUN mkdir -p ${repos_dir}

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/functest ${repos_dir}/functest
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${repos_dir}/releng
RUN git clone https://github.com/openstack/rally.git ${repos_dir}/rally
RUN git clone https://github.com/opendaylight/integration.git ${repos_dir}/odl_integration
RUN git clone -b stable https://github.com/boucherv-orange/clearwater-live-test ${repos_dir}/vims-test

RUN pip install -r ${repos_dir}/functest/docker/requirements.pip

RUN gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
RUN curl -L https://get.rvm.io | bash -s stable
RUN bash -c 'source /etc/profile.d/rvm.sh ; rvm autolibs enable ; rvm install 1.9.3 ; rvm use 1.9.3'
RUN bash -c 'source /etc/profile.d/rvm.sh ; cd ${repos_dir}/vims-test ; bundle install'

ADD http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img /home/opnfv/functest/data/