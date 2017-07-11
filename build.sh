#!/bin/bash

set -e

repo=${repo:-opnfv}

(cd docker && docker build -t "${repo}/functest" .)
docker push "${repo}/functest"

for dir in docker/core docker/healthcheck docker/smoke; do
    (cd ${dir} && docker build -t "${repo}/functest-${dir##**/}" .)
    docker push "${repo}/functest-${dir##**/}"
done

exit $?
