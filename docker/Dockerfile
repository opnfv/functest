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
#    $ docker run -t -i -e "INSTALLER_TYPE=fuel/foreman" \
#      -e "INSTALLER_IP=10.20.0.2/172.30.10.73" opnfv/functest
#


FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

ENV repos_dir /home/opnfv/repos

# Packaged dependencies
RUN apt-get update && apt-get install -y \
ssh \
sshpass \
git \
gcc \
wget \
python-dev \
python-pip \
postgresql \
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

RUN pip install -r ${repos_dir}/functest/docker/requirements.pip
