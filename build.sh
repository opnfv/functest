#!/bin/bash

set -e

(cd docker && docker build -t opnfv/functest .)
docker push opnfv/functest

for dir in docker/core docker/healthcheck docker/smoke; do
  (cd $dir && docker build -t opnfv/functest-$(basename $dir) .)
  #docker push opnfv/functest-$(basename $dir)
done

exit $?
